"""
Task 4 – Data processing and merging

Skripta spaja sve CSV datoteke u "processed_data.csv" uz potrebne transformacije.

Obrada se radi u dva prolaza:
1. Pronalaze se korisnici iz Germany i Italy koji imaju "drawer_action" event.
2. Podaci se ponovno čitaju i filtriraju (datum, korisnici), zadržavaju se
   samo traženi stupci te se preimenuju u camelCase.

Podaci se obrađuju u chunkovima radi bolje kontrole memorije.
"""

import logging
import sys
from pathlib import Path

import pandas as pd

from helpers import setup_logging


RAW_DATA_DIR = Path("data/raw_data")
OUTPUT_DIR = Path("data/processed_data")
OUTPUT_FILE = OUTPUT_DIR / "processed_data.csv"

CUTOFF_DATE = "20240315"
CHUNK_SIZE = 50_000

# stupci iz bq.events tablice
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


def get_csv_files():
    files = sorted(
        file_path
        for file_path in RAW_DATA_DIR.rglob("*.csv")
        if not file_path.name.startswith(".")
    )

    if not files:
        raise FileNotFoundError(f"Nema CSV datoteka u {RAW_DATA_DIR}")

    logging.info("Pronađeno %d CSV datoteka.", len(files))
    return files


def read_csv_in_chunks(csv_path: Path, usecols=None):
    return pd.read_csv(
        csv_path,
        header=None,              # predpostavka je da CSV datoteke nemaju header
        names=SOURCE_COLUMNS,     # također ručno dodajemo nazive stupaca
        usecols=usecols,
        chunksize=CHUNK_SIZE,
        dtype=str,
        low_memory=False,
    )


def find_users_to_remove(csv_files):
    users_to_remove = set()

    for csv_file in csv_files:
        logging.info("Analiziram korisnike za izbacivanje iz datoteke: %s", csv_file)

        for chunk in read_csv_in_chunks(
            csv_file,
            usecols=["event_date", "event_name", "user_pseudo_id", "geo_country"],
        ):
            # Radimo samo s podacima koji ulaze u finalni output.
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    first_write = True

    for csv_file in csv_files:
        logging.info("Obrađujem datoteku: %s", csv_file)

        for chunk in read_csv_in_chunks(csv_file, usecols=USED_COLUMNS):
            # Zadrži samo datume <= CUTOFF_DATE
            chunk = chunk[chunk["event_date"] <= CUTOFF_DATE]

            # Izbaci sve zapise korisnika koji upadaju u traženi uvjet.
            chunk = chunk[~chunk["user_pseudo_id"].isin(users_to_remove)]

            if chunk.empty:
                continue

            # Preimenuj stupce u camelCase.
            chunk = chunk.rename(columns=OUTPUT_COLUMNS)

            chunk.to_csv(
                OUTPUT_FILE,
                mode="w" if first_write else "a",
                index=False,
                header=first_write,
            )

            first_write = False

    if first_write:
        # Ako ništa nije upisano, i dalje kreiraj prazan CSV s headerom.
        empty_df = pd.DataFrame(columns=list(OUTPUT_COLUMNS.values()))
        empty_df.to_csv(OUTPUT_FILE, index=False)

    logging.info("Processed datoteka spremljena u: %s", OUTPUT_FILE)


def main():
    setup_logging()

    try:
        csv_files = get_csv_files()
        users_to_remove = find_users_to_remove(csv_files)
        process_and_merge(csv_files, users_to_remove)

        logging.info("Task 4 uspješno završen.")
        return 0

    except Exception as e:
        logging.exception("Task 4 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())