# Task 1 - ClickHouse + Grafana with Docker Compose

Ovaj folder sadrži sve potrebno za lokalno pokretanje ClickHouse baze podataka i Grafane pomoću Docker Compose-a.

Cilj je omogućiti jednostavno podizanje oba servisa i automatsko povezivanje Grafane na ClickHouse kao data source.

---

## Struktura direktorija

```text
HW4/task1/
├── docker-compose.yml
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── clickhouse.yml
└── README.md
```

Objašnjenje:

- docker-compose.yml
  Definira servise (ClickHouse i Grafana), portove, volumene i konfiguraciju.

- grafana/provisioning/datasources/clickhouse.yml
  Konfiguracija koja omogućuje da Grafana automatski prepozna ClickHouse kao data source
  (nije potrebno ručno dodavanje u UI-u).

---

## Servisi

ClickHouse:
- HTTP: http://localhost:8123
- Native TCP: localhost:9000

Grafana:
- URL: http://localhost:3000
- korisničko ime: vrijednost varijable `GRAFANA_ADMIN_USER` (zadano: `admin`)
- lozinka: vrijednost varijable `GRAFANA_ADMIN_PASSWORD`

---

## Pokretanje sustava

Korisnik treba otvoriti terminal u folderu:

```bash
cd HW4/task1
```

Zatim pokrenuti:

```bash
export CLICKHOUSE_PASSWORD="choose-a-local-password" # pragma: allowlist secret
export GRAFANA_ADMIN_PASSWORD="choose-a-different-local-password" # pragma: allowlist secret
docker compose up -d
```

Ova naredba:
- povlači Docker image-e (ako već nisu preuzeti)
- pokreće ClickHouse i Grafanu
- automatski konfigurira datasource u Grafani

---

## Provjera da sve radi

Provjera ClickHouse-a:

```bash
curl http://localhost:8123/ping
```

Očekivani output:

```text
Ok.
```

---

Provjera Grafane:

Korisnik treba otvoriti u browseru:

http://localhost:3000

Login podaci:
- username: vrijednost varijable `GRAFANA_ADMIN_USER` (zadano: `admin`)
- password: vrijednost varijable `GRAFANA_ADMIN_PASSWORD`

Nakon prijave:
- ClickHouse datasource je već konfiguriran
- može se odmah koristiti za izradu dashboarda

---

## Gašenje sustava

Za gašenje servisa:

```bash
docker compose down
```

Ako se želi obrisati i sav spremljeni data (volumes):

```bash
docker compose down -v
```

---

## Napomene

- ClickHouse koristi Docker volumene za persistenciju podataka
  podaci ostaju sačuvani i nakon restarta containera

- ClickHouse bazu i korisnika kreira službeni Docker entrypoint prema varijablama `CLICKHOUSE_DATABASE`, `CLICKHOUSE_USER` i `CLICKHOUSE_PASSWORD`

- portovi su vezani na `127.0.0.1` i nisu izloženi drugim uređajima na mreži

- Grafana automatski učitava datasource iz:

```text
grafana/provisioning/datasources/clickhouse.yml
```

nije potrebno ručno dodavanje datasource-a kroz UI
