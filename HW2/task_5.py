import logging
import os
import sys
from pathlib import Path
import pandas as pd
from clickhouse_driver import Client
from helpers import setup_logging


INPUT_FILE = Path("data/processed_data/processed_data.csv")
CHUNK_SIZE = 100_000

HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
PORT = int(os.getenv("CLICKHOUSE_PORT", "9000"))
USERNAME = os.getenv("CLICKHOUSE_USER", "default")
PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

TABLE_NAME = "fgalic.l2_dataset"


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
ORDER BY eventDate
SETTINGS index_granularity = 8192
"""


def create_client():
    return Client(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
    )


def create_table(client: Client):
    logging.info("Kreiram tablicu ako već ne postoji...")
    client.execute(CREATE_TABLE_QUERY)
    logging.info("Tablica je spremna.")


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
        chunk[column] = chunk[column].where(pd.notna(chunk[column]), None)
        chunk[column] = chunk[column].apply(lambda x: str(x) if x is not None else None)

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
            row.eventDate,
            row.eventName,
            row.userPseudoId,
            row.platform,
            row.status,
            row.geoCountry,
            parsed_id,
        ))

    return records


def upload_data(client: Client):
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Ulazna datoteka ne postoji: {INPUT_FILE}")

    insert_query = f"""
    INSERT INTO {TABLE_NAME}
    (eventDate, eventName, userPseudoId, platform, status, geoCountry, id)
    VALUES
    """

    total_rows = 0

    for chunk_index, chunk in enumerate(
        pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, dtype=str),
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


def main():
    setup_logging()

    try:
        client = create_client()
        create_table(client)
        upload_data(client)

        logging.info("Task 5 uspješno završen.")
        return 0

    except Exception as e:
        logging.exception("Task 5 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
