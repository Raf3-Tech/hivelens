"""Mock fan data for HiveLens.

Generates 500 realistic fan records deterministically. All money values are
integers (cents), never floats.
"""
import random

CITIES = {
    "Los Angeles": (34.0522, -118.2437),
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Toronto": (43.6532, -79.3832),
    "Miami": (25.7617, -80.1918),
    "Austin": (30.2672, -97.7431),
}

GENRES = ["EDM", "Hip Hop", "Rock", "Pop", "Country", "Jazz", "Comedy"]

GENRE_PAIRS = {
    "EDM": ["EDM", "Electronic"],
    "Hip Hop": ["Hip Hop", "Rap"],
    "Rock": ["Rock", "Alternative"],
    "Pop": ["Pop", "Dance"],
    "Country": ["Country", "Folk"],
    "Jazz": ["Jazz", "Blues"],
    "Comedy": ["Comedy", "Live"],
}

FIRST_NAMES = [
    "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Jamie", "Quinn",
    "Skyler", "Dakota", "Reese", "Cameron", "Drew", "Emerson", "Finley", "Harper",
    "Kendall", "Logan", "Parker", "Rowan", "Sawyer", "Sydney", "Alexis", "Bailey",
    "Devon", "Elliot", "Frankie", "Greer", "Hayden", "Indigo", "Jesse", "Kai",
    "Lane", "Marlowe", "Noel", "Oakley", "Phoenix", "River", "Sage", "Tatum",
]

LAST_NAMES = [
    "Pierce", "Nguyen", "Patel", "Garcia", "Kim", "Johnson", "Martinez", "Lee",
    "Brown", "Davis", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Thompson", "White", "Harris", "Clark", "Lewis", "Walker",
    "Hall", "Young", "King", "Wright", "Hill", "Green", "Adams", "Baker",
    "Nelson", "Carter", "Mitchell", "Roberts", "Turner", "Phillips", "Campbell", "Parker",
]


def generate_fans(count: int = 500, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    fans = []
    city_names = list(CITIES.keys())

    for i in range(count):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        name = f"{first} {last}"
        city = rng.choice(city_names)
        base_lat, base_lng = CITIES[city]
        # Jitter within the metro area (~ a few miles)
        lat = round(base_lat + rng.uniform(-0.15, 0.15), 4)
        lng = round(base_lng + rng.uniform(-0.15, 0.15), 4)

        primary_genre = rng.choice(GENRES)
        genres = list(GENRE_PAIRS[primary_genre])
        if rng.random() < 0.3:
            extra = rng.choice(GENRES)
            if extra not in genres:
                genres.append(extra)

        # Spend from $20 to $2000 total
        total_spend_cents = rng.randint(2000, 200000)
        attendance_count = rng.randint(1, 12)
        avg_ticket_spend_cents = max(1000, total_spend_cents // attendance_count)
        last_purchase_days_ago = rng.randint(1, 730)
        email_open_rate = round(rng.uniform(0.05, 0.85), 2)
        email_status = rng.choices(
            ["active", "unsubscribed", "bounced"], weights=[80, 12, 8]
        )[0]

        fans.append({
            "id": f"fan_{i + 1:03d}",
            "name": name,
            "email": f"{first.lower()}.{last.lower()}{i}@example.com",
            "phone": f"+1-555-{rng.randint(0, 9999):04d}",
            "city": city,
            "lat": lat,
            "lng": lng,
            "age": rng.randint(18, 65),
            "gender": rng.choice(["F", "M", "X"]),
            "total_spend_cents": total_spend_cents,
            "avg_ticket_spend_cents": avg_ticket_spend_cents,
            "attendance_count": attendance_count,
            "last_purchase_days_ago": last_purchase_days_ago,
            "genres": genres,
            "email_open_rate": email_open_rate,
            "email_status": email_status,
        })

    return fans


# Pre-generated fixture available on import
FIXTURE_FANS = generate_fans(500)


if __name__ == "__main__":
    fans = generate_fans(500)
    print(f"Generated {len(fans)} fans")
    print(fans[0])
