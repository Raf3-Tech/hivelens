"""Fan segmentation engine for HiveLens.

No external libraries — haversine distance is implemented inline.
"""
import math


class FanSegmenter:
    AUTO_SEGMENTS = ["vip", "lapsed", "first_timer", "high_spender", "local"]

    def segment_all(self, fans: list[dict], event_lat: float, event_lng: float) -> dict:
        """Returns dict of segment_name -> list of fan ids."""
        result = {name: [] for name in self.AUTO_SEGMENTS}

        for fan in fans:
            fid = fan["id"]

            if fan["total_spend_cents"] > 50000 or fan["attendance_count"] >= 5:
                result["vip"].append(fid)

            if fan["last_purchase_days_ago"] > 365:
                result["lapsed"].append(fid)

            if fan["attendance_count"] == 1:
                result["first_timer"].append(fid)

            if fan["avg_ticket_spend_cents"] > 15000:
                result["high_spender"].append(fid)

            dist = self._haversine_miles(fan["lat"], fan["lng"], event_lat, event_lng)
            if dist < 25:
                result["local"].append(fid)

        return result

    def apply_custom_filter(self, fans: list[dict], filters: dict) -> list[str]:
        """Filter fans against the custom filter schema. Returns matching fan ids."""
        genres = filters.get("genres")
        cities = filters.get("cities")
        min_spend = filters.get("min_spend_cents")
        max_spend = filters.get("max_spend_cents")
        min_attendance = filters.get("min_attendance")
        max_last_purchase = filters.get("max_last_purchase_days")
        email_status = filters.get("email_status")
        radius_miles = filters.get("radius_miles")
        event_lat = filters.get("event_lat")
        event_lng = filters.get("event_lng")

        matched = []
        for fan in fans:
            if genres and not any(g in fan["genres"] for g in genres):
                continue
            if cities and fan["city"] not in cities:
                continue
            if min_spend is not None and fan["total_spend_cents"] < min_spend:
                continue
            if max_spend is not None and fan["total_spend_cents"] > max_spend:
                continue
            if min_attendance is not None and fan["attendance_count"] < min_attendance:
                continue
            if max_last_purchase is not None and fan["last_purchase_days_ago"] > max_last_purchase:
                continue
            if email_status and fan["email_status"] != email_status:
                continue
            if radius_miles is not None and event_lat is not None and event_lng is not None:
                dist = self._haversine_miles(fan["lat"], fan["lng"], event_lat, event_lng)
                if dist > radius_miles:
                    continue
            matched.append(fan["id"])

        return matched

    def _haversine_miles(self, lat1, lng1, lat2, lng2) -> float:
        """Great-circle distance in miles. No external libs."""
        r = 3958.8  # Earth radius in miles
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lng2 - lng1)
        a = (math.sin(d_phi / 2) ** 2
             + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c
