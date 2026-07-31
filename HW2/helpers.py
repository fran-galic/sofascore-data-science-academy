import logging
import os
import tarfile
import time
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import paramiko


HOST = os.getenv("SSH_HOST", "")
USERNAME = os.getenv("SSH_USERNAME", "")
PASSWORD = os.getenv("SSH_PASSWORD", "")

RAW_DATA_DIR = Path("data/raw_data")
RETRIES = 3
RETRY_DELAY = 2


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def create_ssh_client():
    missing = [
        name
        for name, value in {
            "SSH_HOST": HOST,
            "SSH_USERNAME": USERNAME,
            "SSH_PASSWORD": PASSWORD,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return client


def run_with_retries(action, error_message: str):
    last_error = None

    for attempt in range(1, RETRIES + 1):
        try:
            logging.info("Spajam se na server... pokušaj %d/%d", attempt, RETRIES)
            return action()
        except Exception as e:
            last_error = e
            logging.warning("%s %s", error_message, e)

            if attempt < RETRIES:
                logging.info("Ponovni pokušaj za %d sekunde...", RETRY_DELAY)
                time.sleep(RETRY_DELAY)

    raise RuntimeError(error_message) from last_error


def download_file(remote_file_path: str, local_file_path: Path):
    def action():
        client = None
        try:
            client = create_ssh_client()
            client.connect(
                hostname=HOST,
                username=USERNAME,
                password=PASSWORD,
                timeout=10,
            )

            with client.open_sftp() as sftp:
                # Provjera da datoteka postoji prije preuzimanja.
                sftp.stat(remote_file_path)
                logging.info("Preuzimam datoteku %s", remote_file_path)
                sftp.get(remote_file_path, str(local_file_path))

            logging.info("Preuzimanje uspješno završeno.")
        finally:
            if client is not None:
                client.close()

    try:
        run_with_retries(action, "Preuzimanje nije uspjelo.")
    except Exception:
        if local_file_path.exists():
            local_file_path.unlink(missing_ok=True)
        raise


def download_files(remote_dir_path: str, local_dir_path: Path, extension: str = ".zip"):
    def action():
        client = None
        downloaded_files = []

        try:
            client = create_ssh_client()
            client.connect(
                hostname=HOST,
                username=USERNAME,
                password=PASSWORD,
                timeout=10,
            )

            with client.open_sftp() as sftp:
                file_names = sorted(
                    name for name in sftp.listdir(remote_dir_path)
                    if name.endswith(extension)
                )

                if not file_names:
                    raise FileNotFoundError(
                        f"U folderu {remote_dir_path} nema {extension} datoteka."
                    )

                logging.info("Pronađeno %d datoteka za preuzimanje.", len(file_names))

                for file_name in file_names:
                    remote_file_path = f"{remote_dir_path}/{file_name}"
                    local_file_path = local_dir_path / file_name

                    logging.info("Preuzimam %s", remote_file_path)
                    sftp.get(remote_file_path, str(local_file_path))
                    downloaded_files.append(file_name)

            logging.info("Preuzimanje svih datoteka uspješno završeno.")
            return downloaded_files

        finally:
            if client is not None:
                client.close()

    try:
        return run_with_retries(action, "Preuzimanje datoteka iz foldera nije uspjelo.")
    except Exception:
        for file_path in local_dir_path.glob(f"*{extension}"):
            file_path.unlink(missing_ok=True)
        raise


def extract_zip(zip_path: Path, extract_dir: Path):
    try:
        with ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(extract_dir)
        logging.info("Raspakiravanje ZIP datoteke uspješno završeno.")
    except BadZipFile as e:
        raise RuntimeError("ZIP datoteka je neispravna.") from e


def extract_tar_gz(tar_path: Path, extract_dir: Path):
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(extract_dir)
        logging.info("Raspakiravanje TAR.GZ datoteke uspješno završeno.")
    except tarfile.TarError as e:
        raise RuntimeError("TAR.GZ datoteka je neispravna.") from e
