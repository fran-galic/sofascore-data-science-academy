import logging
import os
import sys
from pathlib import Path

import pandas as pd
from clickhouse_driver import Client

from helpers import download_files, extract_zip, setup_logging


BASE_DIR = Path("/app")
RAW_DIR = BASE_DIR / "data" / "raw_data" / "march"
PROCESSED_DIR = BASE_DIR / "data" / "processed_data"
PROCESSED_FILE = PROCESSED_DIR / "processed_data.csv"

SSH_HOST = os.getenv("SSH_HOST", "")
SSH_USERNAME = os.getenv("SSH_USERNAME", "")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", "")
REMOTE_DIR_PATH = os.getenv("REMOTE_DIR_PATH", "")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "host.docker.internal")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "9000"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "default")
CLICKHOUSE_TABLE = os.getenv("CLICKHOUSE_TABLE", "l4_dataset")

CUTOFF_DATE = os.getenv("CUTOFF_DATE", "20240315")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "50000"))
INSERT_CHUNK_SIZE = int(os.getenv("INSERT_CHUNK_SIZE", "100000"))

SOURCE_COLUMNS = [
    "event_date",
    "event_timestamp",
    "event_name",
    "user_pseudo_id",
    "geo_country",
    "app_info_version",
    "platform",
    "status",
    "id",
    "event_id",
    "name",
    "item_name",
    "previous_first_open_count",
    "firebase_experiments",
]

USED_COLUMNS = [
    "event_date",
    "event_name",
    "user_pseudo_id",
    "platform",
    "status",
    "geo_country",
    "id",
]

OUTPUT_COLUMNS = {
    "event_date": "eventDate",
    "event_name": "eventName",
    "user_pseudo_id": "userPseudoId",
    "platform": "platform",
    "status": "status",
    "geo_country": "geoCountry",
    "id": "id",
}

TABLE_NAME = f"{CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}"

CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    eventDate String,
    eventName String,
    userPseudoId String,
    platform LowCardinality(String),
    status LowCardinality(String),
    geoCountry LowCardinality(String),
    id Nullable(Int64)
)
ENGINE = MergeTree()
ORDER BY (eventDate, eventName, geoCountry, platform)
SETTINGS index_granularity = 8192
"""


def ensure_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_raw_dir():
    for path in RAW_DIR.glob("*"):
        if path.is_file():
            path.unlink(missing_ok=True)


def get_csv_files():
    files = sorted(
        file_path
        for file_path in RAW_DIR.rglob("*.csv")
        if not file_path.name.startswith(".")
    )

    if not files:
        raise FileNotFoundError(f"Nema CSV datoteka u {RAW_DIR}")

    logging.info("Pronađeno %d CSV datoteka.", len(files))
    return files


def read_csv_in_chunks(csv_path: Path, usecols=None):
    return pd.read_csv(
        csv_path,
        header=None,
        names=SOURCE_COLUMNS,
        usecols=usecols,
        chunksize=CHUNK_SIZE,
        dtype=str,
        low_memory=False,
    )


def download_and_extract():
    missing = [
        name
        for name, value in {
            "SSH_HOST": SSH_HOST,
            "SSH_USERNAME": SSH_USERNAME,
            "SSH_PASSWORD": SSH_PASSWORD,
            "REMOTE_DIR_PATH": REMOTE_DIR_PATH,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    cleanup_raw_dir()

    downloaded_files = download_files(
        REMOTE_DIR_PATH,
        RAW_DIR,
        ".zip",
        host=SSH_HOST,
        username=SSH_USERNAME,
        password=SSH_PASSWORD,
    )

    for file_name in downloaded_files:
        extract_zip(RAW_DIR / file_name, RAW_DIR)


def find_users_to_remove(csv_files):
    users_to_remove = set()

    for csv_file in csv_files:
        logging.info("Analiziram korisnike za izbacivanje iz datoteke: %s", csv_file)

        for chunk in read_csv_in_chunks(
            csv_file,
            usecols=["event_date", "event_name", "user_pseudo_id", "geo_country"],
        ):
            chunk = chunk[chunk["event_date"] <= CUTOFF_DATE]

            mask = (
                chunk["geo_country"].isin(["Germany", "Italy"])
                & (chunk["event_name"] == "drawer_action")
            )

            matched_users = chunk.loc[mask, "user_pseudo_id"].dropna().unique()
            users_to_remove.update(matched_users)

    logging.info("Pronađeno %d korisnika koje treba izbaciti.", len(users_to_remove))
    return users_to_remove


def process_and_merge(csv_files, users_to_remove):
    if PROCESSED_FILE.exists():
        PROCESSED_FILE.unlink()

    first_write = True

    for csv_file in csv_files:
        logging.info("Obrađujem datoteku: %s", csv_file)

        for chunk in read_csv_in_chunks(csv_file, usecols=USED_COLUMNS):
            chunk = chunk[chunk["event_date"] <= CUTOFF_DATE]
            chunk = chunk[~chunk["user_pseudo_id"].isin(users_to_remove)]

            if chunk.empty:
                continue

            chunk = chunk.rename(columns=OUTPUT_COLUMNS)

            chunk.to_csv(
                PROCESSED_FILE,
                mode="w" if first_write else "a",
                index=False,
                header=first_write,
            )

            first_write = False

    if first_write:
        pd.DataFrame(columns=list(OUTPUT_COLUMNS.values())).to_csv(
            PROCESSED_FILE,
            index=False,
        )

    logging.info("Processed datoteka spremljena u: %s", PROCESSED_FILE)


def create_client():
    return Client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )


def create_table(client: Client):
    logging.info("Kreiram tablicu ako već ne postoji...")
    client.execute(CREATE_TABLE_QUERY)
    logging.info("Tablica je spremna.")


def truncate_table(client: Client):
    logging.info("Praznim tablicu prije importa...")
    client.execute(f"TRUNCATE TABLE {TABLE_NAME}")
    logging.info("Tablica ispražnjena.")


def prepare_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.copy()

    string_columns = [
        "eventDate",
        "eventName",
        "userPseudoId",
        "platform",
        "status",
        "geoCountry",
    ]

    for column in string_columns:
        chunk[column] = chunk[column].fillna("").astype(str)

    return chunk


def build_records(chunk: pd.DataFrame):
    records = []

    for row in chunk.itertuples(index=False):
        raw_id = row.id

        if pd.isna(raw_id) or raw_id in ("", "nan", "None"):
            parsed_id = None
        else:
            parsed_id = int(float(raw_id))

        records.append((
            str(row.eventDate) if row.eventDate is not None else "",
            str(row.eventName) if row.eventName is not None else "",
            str(row.userPseudoId) if row.userPseudoId is not None else "",
            str(row.platform) if row.platform is not None else "",
            str(row.status) if row.status is not None else "",
            str(row.geoCountry) if row.geoCountry is not None else "",
            parsed_id,
        ))

    return records


def upload_data(client: Client):
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(f"Ulazna datoteka ne postoji: {PROCESSED_FILE}")

    insert_query = f"""
    INSERT INTO {TABLE_NAME}
    (eventDate, eventName, userPseudoId, platform, status, geoCountry, id)
    VALUES
    """

    total_rows = 0

    for chunk_index, chunk in enumerate(
        pd.read_csv(PROCESSED_FILE, chunksize=INSERT_CHUNK_SIZE, dtype=str),
        start=1,
    ):
        prepared_chunk = prepare_chunk(chunk)
        records = build_records(prepared_chunk)

        if not records:
            continue

        logging.info("Šaljem chunk %d s %d redaka...", chunk_index, len(records))
        client.execute(insert_query, records, types_check=True)

        total_rows += len(records)
        logging.info("Dosad učitano %d redaka.", total_rows)

    logging.info("Upload završen. Ukupno učitano %d redaka.", total_rows)


def verify_import(client: Client):
    count = client.execute(f"SELECT count() FROM {TABLE_NAME}")[0][0]
    logging.info("Verifikacija importa: tablica %s ima %d redaka.", TABLE_NAME, count)
    return count


def main():
    setup_logging()
    ensure_directories()

    try:
        download_and_extract()
        csv_files = get_csv_files()
        users_to_remove = find_users_to_remove(csv_files)
        process_and_merge(csv_files, users_to_remove)

        client = create_client()
        create_table(client)
        truncate_table(client)
        upload_data(client)
        verify_import(client)

        logging.info("Task 2 uspješno završen.")
        return 0

    except Exception as e:
        logging.exception("Task 2 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
