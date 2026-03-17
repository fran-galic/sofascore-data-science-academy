import logging
import sys
from pathlib import Path

from helpers import download_files, extract_zip, setup_logging


REMOTE_DIR_PATH = "/home/dsa/dataset/march"
MARCH_DIR = Path("data/raw_data/march")


def main():
    setup_logging()
    MARCH_DIR.mkdir(parents=True, exist_ok=True)

    try:
        downloaded_files = download_files(REMOTE_DIR_PATH, MARCH_DIR, ".zip")

        for file_name in downloaded_files:
            extract_zip(MARCH_DIR / file_name, MARCH_DIR)

        logging.info("Task 3 uspješno završen.")
        return 0
    except Exception as e:
        logging.exception("Task 3 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())