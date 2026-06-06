"""HiveLens Flask backend.

Demo data (fans + pre-generated campaigns) is served from PostgreSQL. If the
database is unreachable, the app transparently falls back to the in-memory
fixture so it still runs for a quick demo. Campaign copy comes from Claude when
ANTHROPIC_API_KEY is set, otherwise from the pre-generated library in the DB.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import db
from mock_data import FIXTURE_FANS
from segmenter import FanSegmenter
from campaign import CampaignGenerator

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

segmenter = FanSegmenter()

# In-memory session store (working set loaded from the DB on ingest)
STATE = {
    "fans": [],
    "by_id": {},
    "segments": {},          # segment_name -> [fan_ids]
    "event": {"lat": None, "lng": None},
    "fan_source": None,       # "database" | "fixture"
}

# Rotates pre-generated campaign variants per (segment, event) so repeated
# "Regenerate" clicks return fresh-feeling copy.
_DB_ROTATION: dict[tuple, int] = {}


def _index_fans(fans: list[dict]) -> None:
    STATE["fans"] = fans
    STATE["by_id"] = {f["id"]: f for f in fans}


def _try_init_db() -> bool:
    """Ensure schema exists and return True if the DB is reachable."""
    try:
        conn = db.get_conn()
        db.init_schema(conn)
        conn.close()
        return True
    except Exception as e:
        app.logger.warning("Postgres unavailable, using in-memory fixture: %s", e)
        return False


DB_AVAILABLE = _try_init_db()


@app.route("/api/ingest", methods=["POST"])
def ingest():
    body = request.get_json(silent=True) or {}

    if body.get("use_fixture"):
        fans, source = _load_demo_fans()
    elif body.get("fans"):
        fans, source = body["fans"], "upload"
    else:
        fans, source = [], "empty"

    _index_fans(fans)
    STATE["fan_source"] = source
    return jsonify({
        "fan_count": len(fans),
        "source": source,
        "message": f"Ingested {len(fans)} fans from {source}",
    })


def _load_demo_fans():
    """Prefer the seeded Postgres dataset; fall back to the in-memory fixture."""
    if DB_AVAILABLE:
        try:
            conn = db.get_conn()
            try:
                fans = db.load_fans(conn)
            finally:
                conn.close()
            if fans:
                return fans, "database"
        except Exception as e:
            app.logger.warning("DB fan load failed, using fixture: %s", e)
    return list(FIXTURE_FANS), "fixture"


@app.route("/api/segments", methods=["POST"])
def segments():
    body = request.get_json(silent=True) or {}
    event_lat = body.get("event_lat")
    event_lng = body.get("event_lng")
    STATE["event"] = {"lat": event_lat, "lng": event_lng}

    fans = STATE["fans"]
    seg_ids = segmenter.segment_all(fans, event_lat, event_lng)
    STATE["segments"] = seg_ids

    segments_out = {
        name: {"count": len(ids), "fan_ids": ids}
        for name, ids in seg_ids.items()
    }
    return jsonify({"segments": segments_out, "total_fans": len(fans)})


@app.route("/api/segment/custom", methods=["POST"])
def segment_custom():
    body = request.get_json(silent=True) or {}
    filters = body.get("filters", {})
    fan_ids = segmenter.apply_custom_filter(STATE["fans"], filters)
    sample = [STATE["by_id"][fid] for fid in fan_ids[:3]]
    return jsonify({"count": len(fan_ids), "fan_ids": fan_ids, "sample": sample})


@app.route("/api/fans/sample", methods=["GET"])
def fans_sample():
    segment = request.args.get("segment", "")
    limit = int(request.args.get("limit", 5))
    ids = STATE["segments"].get(segment, [])
    fans = [STATE["by_id"][fid] for fid in ids[:limit]]
    return jsonify({"fans": fans})


def _db_campaign(segment: str, event_name: str, fan_count: int):
    """Serve a rotating pre-generated campaign from Postgres, or None on miss."""
    if not DB_AVAILABLE:
        return None
    try:
        conn = db.get_conn()
        try:
            variants = db.get_campaign_variants(conn, segment, event_name)
        finally:
            conn.close()
    except Exception as e:
        app.logger.warning("DB campaign lookup failed: %s", e)
        return None

    if not variants:
        return None

    key = (segment, event_name)
    idx = (_DB_ROTATION.get(key, -1) + 1) % len(variants)
    _DB_ROTATION[key] = idx
    v = variants[idx]
    return {
        "subject_line": v["subject_line"],
        "email_body": v["email_body"],
        "sms_body": v["sms_body"],
        "send_estimate": fan_count,
        "projected_open_rate": v["projected_open_rate"],
        "ai_generated": False,
        "source": "database",
    }


@app.route("/api/campaign/generate", methods=["POST"])
def campaign_generate():
    body = request.get_json(silent=True) or {}
    segment = body.get("segment")
    event_name = body.get("event_name", "")
    event_date = body.get("event_date", "")
    event_city = body.get("event_city", "")
    event_lat = body.get("event_lat")
    event_lng = body.get("event_lng")

    # Resolve fan ids: known auto-segment, or custom filters
    if segment in STATE["segments"]:
        fan_ids = STATE["segments"][segment]
    elif body.get("fan_ids"):
        fan_ids = body["fan_ids"]
    else:
        seg_ids = segmenter.segment_all(STATE["fans"], event_lat, event_lng)
        STATE["segments"] = seg_ids
        fan_ids = seg_ids.get(segment, [])

    fan_count = len(fan_ids)
    sample_fans = [STATE["by_id"][fid] for fid in fan_ids[:5] if fid in STATE["by_id"]]

    generator = CampaignGenerator()
    source = "template"

    if generator.has_key:
        result = generator.generate(
            segment=segment, event_name=event_name, event_date=event_date,
            event_city=event_city, fan_count=fan_count, sample_fans=sample_fans,
        )
        source = "claude" if result.get("ai_generated") else "template"
    else:
        # No API key: serve the pre-generated library from Postgres, falling
        # back to live-rendered templates on a miss (e.g. a custom event name).
        result = _db_campaign(segment, event_name, fan_count)
        if result is not None:
            source = "database"
        else:
            result = generator.generate(
                segment=segment, event_name=event_name, event_date=event_date,
                event_city=event_city, fan_count=fan_count, sample_fans=sample_fans,
            )
            source = "template"

    return jsonify({
        "segment": segment,
        "fan_count": fan_count,
        "subject_line": result["subject_line"],
        "email_body": result["email_body"],
        "sms_body": result["sms_body"],
        "send_estimate": result["send_estimate"],
        "projected_open_rate": result["projected_open_rate"],
        "ai_generated": result["ai_generated"],
        "source": source,
    })


@app.route("/api/health", methods=["GET"])
def health():
    db_fans = None
    if DB_AVAILABLE:
        try:
            conn = db.get_conn()
            try:
                db_fans = db.fan_count(conn)
            finally:
                conn.close()
        except Exception:
            db_fans = None
    return jsonify({
        "status": "ok",
        "fans_loaded": len(STATE["fans"]),
        "fan_source": STATE["fan_source"],
        "db_available": DB_AVAILABLE,
        "db_fan_count": db_fans,
    })


if __name__ == "__main__":
    # use_reloader disabled: the reloader spawns a child process that can
    # outlive restarts and hold the port. Single process is simpler to manage.
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
