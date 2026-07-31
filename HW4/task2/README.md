# Task 2 - Dockerized March 2024 import u ClickHouse

Ovaj task implementira cijeli data pipeline iz HW2 zadataka 3, 4 i 5, te ga pokreće unutar Docker okruženja.

Pipeline uključuje sljedeće korake:
1. preuzimanje (download) March 2024 ZIP datoteka sa servera
2. raspakiravanje (extract) CSV datoteka
3. obradu i filtriranje podataka
4. upload u ClickHouse tablicu `l4_dataset`

---

## Struktura direktorija

```text
HW4/task2/
├── docker-compose-import.yml
├── README.md
└── importer/
    ├── Dockerfile
    ├── requirements.txt
    ├── helpers.py
    ├── import_march_2024.py
    └── data/
```

---

## Bitna pretpostavka

Prije pokretanja ovog taska potrebno je imati pokrenut ClickHouse.

Ako se koristi rješenje iz Task 1, potrebno je prvo pokrenuti:

```bash
cd HW4/task1
docker compose up -d
```

---

## Pokretanje importa

Korisnik treba otvoriti terminal u folderu:

```bash
cd HW4/task2
```

Zatim pokrenuti:

```bash
export SSH_HOST="your-ssh-host"
export SSH_USERNAME="your-ssh-user"
export SSH_PASSWORD="your-ssh-password" # pragma: allowlist secret
export REMOTE_DIR_PATH="your-remote-directory"
docker compose -f docker-compose-import.yml up --build
```

Ova naredba:
- builda Docker image za importer
- pokreće container
- izvršava cijeli pipeline (download → processing → upload)

---

## Provjera uspješnosti importa

Ako je ClickHouse pokrenut kroz Docker iz Task 1:

```bash
docker exec -it hw4-clickhouse clickhouse-client --user "${CLICKHOUSE_USER:-fgalic}" --password --query "SELECT count() FROM fgalic.l4_dataset"
```

Ako korisnik ima lokalno instaliran `clickhouse-client`:

```bash
clickhouse-client --host 127.0.0.1 --port 9000 --user "${CLICKHOUSE_USER:-fgalic}" --password --query "SELECT count() FROM fgalic.l4_dataset"
```

Ako je import uspješan, upit će vratiti broj redaka u tablici.

---

## Napomena o konekciji iz containera

Importer koristi sljedeću konfiguraciju za spajanje na ClickHouse:

```text
CLICKHOUSE_HOST=host.docker.internal
```

Uz dodatno `extra_hosts` mapiranje na `host-gateway`.

Ovo omogućuje Docker containeru da pristupi servisima koji su pokrenuti na host stroju.

---

## Promjena konfiguracije (user / baza / tablica)

Ako je potrebno koristiti druge postavke, korisnik može promijeniti environment varijable u datoteci:

```text
docker-compose-import.yml
```

Relevantne varijable su:
- SSH_HOST
- SSH_USERNAME
- SSH_PASSWORD
- REMOTE_DIR_PATH
- CLICKHOUSE_HOST
- CLICKHOUSE_PORT
- CLICKHOUSE_USER
- CLICKHOUSE_PASSWORD
- CLICKHOUSE_DATABASE
- CLICKHOUSE_TABLE

Stvarne pristupne podatke treba postaviti samo u lokalnom okruženju. Ne treba ih zapisivati u ovu datoteku ni u Docker Compose konfiguraciju.
