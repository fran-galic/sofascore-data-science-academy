import logging
import time
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import paramiko


RETRIES = 3
RETRY_DELAY = 2


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def create_ssh_client():
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


def download_files(remote_dir_path: str, local_dir_path: Path, extension: str = ".zip", *, host: str, username: str, password: str):
    def action():
        client = None
        downloaded_files = []

        try:
            client = create_ssh_client()
            client.connect(
                hostname=host,
                username=username,
                password=password,
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
        logging.info("Raspakiravanje ZIP datoteke uspješno završeno: %s", zip_path.name)
    except BadZipFile as e:
        raise RuntimeError(f"ZIP datoteka je neispravna: {zip_path}") from e
