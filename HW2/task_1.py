import logging
import sys
from pathlib import Path

from helpers import download_file, extract_zip, setup_logging


REMOTE_FILE_PATH = "/home/dsa/dataset/january.csv.zip"
JANUARY_DIR = Path("data/raw_data/january")


def main():
    setup_logging()
    JANUARY_DIR.mkdir(parents=True, exist_ok=True)

    local_zip_path = JANUARY_DIR / "january.csv.zip"

    try:
        download_file(REMOTE_FILE_PATH, local_zip_path)
        extract_zip(local_zip_path, JANUARY_DIR)
        logging.info("Task 1 uspješno završen.")
        return 0
    except Exception as e:
        logging.exception("Task 1 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())