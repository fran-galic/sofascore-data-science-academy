-- Connection values below are placeholders. Replace them locally before execution;
-- never commit real credentials to the repository.
-- postoji samo mali broj sportova, zato koristim FLAT layout.
CREATE DICTIONARY fgalic.sport_dictionary
(
    id UInt64,
    name Nullable(String),
    slug Nullable(String),
    externalid Nullable(Int32)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'sport'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(FLAT())
LIFETIME(MIN 0 MAX 1000);


-- Za sve ostalo koristim HASHED jer se radi o većem broju lookupu po id-u.
CREATE DICTIONARY fgalic.event_dictionary
(
    id UInt64,
    sport_id Nullable(Int32),
    tournament_id Nullable(Int32),
    season_id Nullable(Int32),
    venue_id Nullable(Int32),
    referee_id Nullable(Int32),
    attendance Nullable(Int32),
    startdate Nullable(DateTime64(6)),
    hometeam_id Nullable(Int32),
    awayteam_id Nullable(Int32)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'event'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(HASHED())
LIFETIME(MIN 0 MAX 1000);


CREATE DICTIONARY fgalic.tournament_dictionary
(
    id UInt64,
    uniquetournament_id Nullable(Int32),
    name Nullable(String),
    slug Nullable(String)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'tournament'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(HASHED())
LIFETIME(MIN 0 MAX 1000);


CREATE DICTIONARY fgalic.uniquetournament_dictionary
(
    id UInt64,
    name Nullable(String),
    slug Nullable(String),
    priority Nullable(Int32),
    "order" Nullable(Int32),
    externalid Nullable(Int32),
    externaltype Nullable(Int16),
    createdat Nullable(DateTime64(6)),
    updatedat Nullable(DateTime64(6)),
    startdate Nullable(DateTime64(6)),
    enddate Nullable(DateTime64(6))
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'uniquetournament'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(FLAT())
LIFETIME(MIN 0 MAX 1000);


CREATE DICTIONARY fgalic.team_dictionary
(
    id UInt64,
    sport_id Nullable(Int32),
    category_id Nullable(Int32),
    tournament_id Nullable(Int32),
    name Nullable(String),
    slug Nullable(String),
    shortname Nullable(String),
    gender Nullable(String)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'team'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(HASHED())
LIFETIME(MIN 0 MAX 1000);


CREATE DICTIONARY fgalic.player_dictionary
(
    id UInt64,
    team_id Nullable(Int32),
    name Nullable(String),
    position Nullable(String),
    weight Nullable(Int32),
    height Nullable(Int32),
    preferredfoot Nullable(String),
    marketvalue Nullable(Int32),
    retired Nullable(UInt8)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    db 'sports'
    table 'player'
    user '<CLICKHOUSE_USER>'
    password '<CLICKHOUSE_PASSWORD>'
))
LAYOUT(HASHED())
LIFETIME(MIN 0 MAX 1000);
