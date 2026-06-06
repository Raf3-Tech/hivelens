"""Seed the HiveLens Postgres database with demo data.

Populates:
  * `fans`      — an ample synthetic fan dataset (default 2000 records)
  * `campaigns` — pre-rendered email/SMS copy for every demo event x segment,
                  so the app serves AI-quality content with no API key.

Usage:
    python seed.py            # seeds 2000 fans
    FAN_COUNT=5000 python seed.py
"""
import os

import db
from mock_data import generate_fans
from demo_events import DEMO_EVENTS
from templates import FALLBACK_TEMPLATES, render
from campaign import PROJECTED_OPEN_RATES

# Template key -> segment name stored in the DB. "_default" backs custom segments.
SEGMENT_KEYS = {
    "vip": "vip",
    "lapsed": "lapsed",
    "first_timer": "first_timer",
    "high_spender": "high_spender",
    "local": "local",
    "_default": "custom",
}


def build_campaign_rows() -> list[dict]:
    rows = []
    for event in DEMO_EVENTS:
        for tmpl_key, segment in SEGMENT_KEYS.items():
            open_rate = PROJECTED_OPEN_RATES.get(segment, 0.35)
            for idx, variant in enumerate(FALLBACK_TEMPLATES[tmpl_key]):
                rows.append({
                    "segment": segment,
                    "event_name": event["name"],
                    "event_date": event["date"],
                    "event_city": event["city"],
                    "variant_idx": idx,
                    "subject_line": render(
                        variant["subject"], event["name"], event["date"], event["city"]
                    )[:60],
                    "email_body": render(
                        variant["email"], event["name"], event["date"], event["city"]
                    ),
                    "sms_body": render(
                        variant["sms"], event["name"], event["date"], event["city"]
                    )[:160],
                    "projected_open_rate": open_rate,
                })
    return rows


def main():
    fan_count = int(os.environ.get("FAN_COUNT", "2000"))
    conn = db.get_conn()
    try:
        db.init_schema(conn)
        db.reset(conn)

        print(f"Generating {fan_count} fans…")
        fans = generate_fans(fan_count)
        db.insert_fans(conn, fans)

        print("Building pre-generated campaign library…")
        rows = build_campaign_rows()
        db.insert_campaigns(conn, rows)

        print("\nSeed complete:")
        print(f"  fans:      {db.fan_count(conn)}")
        print(f"  campaigns: {db.campaign_count(conn)} "
              f"({len(DEMO_EVENTS)} events x {len(SEGMENT_KEYS)} segments)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
