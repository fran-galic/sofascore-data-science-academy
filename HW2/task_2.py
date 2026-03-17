import logging
import sys
from pathlib import Path

from helpers import download_file, extract_tar_gz, setup_logging


REMOTE_FILE_PATH = "/home/dsa/dataset/february.tar.gz"
FEBRUARY_DIR = Path("data/raw_data/events")


def main():
    setup_logging()
    FEBRUARY_DIR.mkdir(parents=True, exist_ok=True)

    local_tar_path = FEBRUARY_DIR / "february.tar.gz"

    try:
        download_file(REMOTE_FILE_PATH, local_tar_path)
        extract_tar_gz(local_tar_path, FEBRUARY_DIR)
        logging.info("Task 2 uspješno završen.")
        return 0
    except Exception as e:
        logging.exception("Task 2 nije uspješno završen: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())