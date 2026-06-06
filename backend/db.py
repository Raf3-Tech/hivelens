"""PostgreSQL data layer for HiveLens.

Holds the demo fan dataset and a library of pre-generated campaign copy so the
app feels AI-powered even without an ANTHROPIC_API_KEY. Connection is taken
from DATABASE_URL (default: a local peer-auth connection to the `hivelens` db).
"""
import os

import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("DATABASE_URL", "dbname=hivelens")

SCHEMA = """
CREATE TABLE IF NOT EXISTS fans (
    id                     TEXT PRIMARY KEY,
    name                   TEXT NOT NULL,
    email                  TEXT NOT NULL,
    phone                  TEXT,
    city                   TEXT NOT NULL,
    lat                    DOUBLE PRECISION NOT NULL,
    lng                    DOUBLE PRECISION NOT NULL,
    age                    INTEGER,
    gender                 TEXT,
    total_spend_cents      INTEGER NOT NULL,
    avg_ticket_spend_cents INTEGER NOT NULL,
    attendance_count       INTEGER NOT NULL,
    last_purchase_days_ago INTEGER NOT NULL,
    genres                 TEXT[] NOT NULL,
    email_open_rate        REAL,
    email_status           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS campaigns (
    id                  SERIAL PRIMARY KEY,
    segment             TEXT NOT NULL,
    event_name          TEXT NOT NULL,
    event_date          TEXT NOT NULL,
    event_city          TEXT NOT NULL,
    variant_idx         INTEGER NOT NULL,
    subject_line        TEXT NOT NULL,
    email_body          TEXT NOT NULL,
    sms_body            TEXT NOT NULL,
    projected_open_rate REAL NOT NULL,
    UNIQUE (segment, event_name, variant_idx)
);

CREATE INDEX IF NOT EXISTS idx_campaigns_lookup
    ON campaigns (segment, event_name);
"""

FAN_COLUMNS = [
    "id", "name", "email", "phone", "city", "lat", "lng", "age", "gender",
    "total_spend_cents", "avg_ticket_spend_cents", "attendance_count",
    "last_purchase_days_ago", "genres", "email_open_rate", "email_status",
]


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()


def reset(conn) -> None:
    """Drop all rows so a re-seed starts clean."""
    with conn.cursor() as cur:
        cur.execute("TRUNCATE fans;")
        cur.execute("TRUNCATE campaigns RESTART IDENTITY;")
    conn.commit()


def fan_count(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fans;")
        return cur.fetchone()[0]


def insert_fans(conn, fans: list[dict]) -> None:
    rows = [
        (
            f["id"], f["name"], f["email"], f.get("phone"), f["city"],
            f["lat"], f["lng"], f.get("age"), f.get("gender"),
            f["total_spend_cents"], f["avg_ticket_spend_cents"],
            f["attendance_count"], f["last_purchase_days_ago"],
            f["genres"], f.get("email_open_rate"), f["email_status"],
        )
        for f in fans
    ]
    with conn.cursor() as cur:
        psycopg2.extras.execute_values(
            cur,
            """INSERT INTO fans
               (id, name, email, phone, city, lat, lng, age, gender,
                total_spend_cents, avg_ticket_spend_cents, attendance_count,
                last_purchase_days_ago, genres, email_open_rate, email_status)
               VALUES %s
               ON CONFLICT (id) DO NOTHING""",
            rows,
        )
    conn.commit()


def load_fans(conn) -> list[dict]:
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"SELECT {', '.join(FAN_COLUMNS)} FROM fans ORDER BY id;")
        # RealDictRow -> plain dict; genres already comes back as a Python list
        return [dict(r) for r in cur.fetchall()]


def insert_campaigns(conn, rows: list[dict]) -> None:
    values = [
        (
            r["segment"], r["event_name"], r["event_date"], r["event_city"],
            r["variant_idx"], r["subject_line"], r["email_body"],
            r["sms_body"], r["projected_open_rate"],
        )
        for r in rows
    ]
    with conn.cursor() as cur:
        psycopg2.extras.execute_values(
            cur,
            """INSERT INTO campaigns
               (segment, event_name, event_date, event_city, variant_idx,
                subject_line, email_body, sms_body, projected_open_rate)
               VALUES %s
               ON CONFLICT (segment, event_name, variant_idx) DO UPDATE SET
                 subject_line = EXCLUDED.subject_line,
                 email_body   = EXCLUDED.email_body,
                 sms_body     = EXCLUDED.sms_body,
                 projected_open_rate = EXCLUDED.projected_open_rate""",
            values,
        )
    conn.commit()


def get_campaign_variants(conn, segment: str, event_name: str) -> list[dict]:
    """All pre-generated variants for a segment+event, ordered by variant_idx."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """SELECT subject_line, email_body, sms_body, projected_open_rate
               FROM campaigns
               WHERE segment = %s AND event_name = %s
               ORDER BY variant_idx""",
            (segment, event_name),
        )
        return [dict(r) for r in cur.fetchall()]


def campaign_count(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM campaigns;")
        return cur.fetchone()[0]
