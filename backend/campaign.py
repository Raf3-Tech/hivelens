"""AI campaign generation for HiveLens, powered by Claude.

If ANTHROPIC_API_KEY is unset or the API call fails, a templated fallback
campaign is returned so the app stays demoable without credentials.
"""
import json
import os

import anthropic

from templates import FALLBACK_TEMPLATES, render as render_template

MODEL = "claude-sonnet-4-20250514"

# Tracks which fallback variant to serve next, per segment, so that each
# regenerate cycles to fresh copy (mimicking live Claude generation).
_VARIANT_ROTATION: dict[str, int] = {}

SEGMENT_PERSONAS = {
    "vip": {
        "tone": "exclusive, appreciative, reward-focused",
        "goal": "reward loyalty, offer early access or upgrades",
        "offer_hint": "early bird presale, VIP package, backstage access",
    },
    "lapsed": {
        "tone": "warm re-engagement, nostalgic, incentive-driven",
        "goal": "win them back with a reason to return",
        "offer_hint": "discount code, 'we miss you' message, new artist lineup",
    },
    "first_timer": {
        "tone": "welcoming, excited, informative",
        "goal": "make them feel like insiders before the event",
        "offer_hint": "what to expect, pro tips, social proof from past events",
    },
    "high_spender": {
        "tone": "premium, aspirational, upsell-ready",
        "goal": "upsell to higher tier tickets or add-ons",
        "offer_hint": "VIP lounge access, meet & greet, premium parking",
    },
    "local": {
        "tone": "energetic, community-focused, urgency-driven",
        "goal": "leverage proximity and day-of convenience",
        "offer_hint": "last minute tickets, bring a friend deal, venue walkthrough",
    },
}

PROJECTED_OPEN_RATES = {
    "vip": 0.52,
    "lapsed": 0.18,
    "first_timer": 0.38,
    "high_spender": 0.45,
    "local": 0.41,
}

PROMPT_TEMPLATE = """You are a marketing copywriter for a music event promotion platform.

Event: {event_name} on {event_date}
Segment: {segment} ({fan_count} fans)
Persona: {tone}
Goal: {goal}
Suggested offer angle: {offer_hint}

Sample fans in this segment:
{sample_json}

Write a personalized campaign for this segment. Return ONLY valid JSON:
{{
  "subject_line": "...",
  "email_body": "...",
  "sms_body": "..."
}}

Rules:
- subject_line: max 60 chars, no emojis
- email_body: 120-160 words, plain text, first name personalization with {{first_name}}
- sms_body: max 160 chars including a short URL placeholder [link]
- Tone must match the segment persona exactly
- Do NOT use generic filler phrases like "exciting opportunity"
"""


class CampaignGenerator:
    def __init__(self):
        self.has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
        # Only build a real client when a key is present; instantiating is cheap
        # but we avoid surprises by gating it on credentials.
        self.client = anthropic.Anthropic() if self.has_key else None

    def generate(self, segment: str, event_name: str, event_date: str,
                 fan_count: int, sample_fans: list[dict],
                 event_city: str = "") -> dict:
        persona = SEGMENT_PERSONAS.get(segment)
        if persona is None:
            # Fallback persona for custom segments
            persona = {
                "tone": "engaging, relevant, action-oriented",
                "goal": "drive ticket conversions for this audience",
                "offer_hint": "tailored ticket offer, limited availability",
            }

        # Trim sample fans to relevant fields to keep the prompt tight
        slim_samples = [
            {
                "name": f.get("name"),
                "city": f.get("city"),
                "genres": f.get("genres"),
                "attendance_count": f.get("attendance_count"),
                "total_spend_cents": f.get("total_spend_cents"),
            }
            for f in sample_fans[:5]
        ]

        event_label = f"{event_name} in {event_city}" if event_city else event_name
        prompt = PROMPT_TEMPLATE.format(
            event_name=event_label,
            event_date=event_date,
            segment=segment,
            fan_count=fan_count,
            tone=persona["tone"],
            goal=persona["goal"],
            offer_hint=persona["offer_hint"],
            sample_json=json.dumps(slim_samples, indent=2),
        )

        if self.client is None:
            data = self._fallback_copy(segment, event_name, event_date, event_city)
            ai_generated = False
        else:
            try:
                message = self.client.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = message.content[0].text.strip()
                data = self._parse_json(raw)
                ai_generated = True
            except Exception:
                data = self._fallback_copy(segment, event_name, event_date, event_city)
                ai_generated = False

        return {
            "subject_line": data.get("subject_line", ""),
            "email_body": data.get("email_body", ""),
            "sms_body": data.get("sms_body", ""),
            "send_estimate": fan_count,
            "projected_open_rate": PROJECTED_OPEN_RATES.get(segment, 0.35),
            "ai_generated": ai_generated,
        }

    @staticmethod
    def _fallback_copy(segment: str, event_name: str, event_date: str,
                       event_city: str = "") -> dict:
        """Templated campaign used when no API key / API is unavailable.

        Picks the next variant in rotation for the segment so repeated calls
        (e.g. "Regenerate") return fresh-feeling copy. Each variant's email is
        hand-tuned to land within the 120-160 word target.
        """
        variants = FALLBACK_TEMPLATES.get(segment) or FALLBACK_TEMPLATES["_default"]
        idx = (_VARIANT_ROTATION.get(segment, -1) + 1) % len(variants)
        _VARIANT_ROTATION[segment] = idx
        variant = variants[idx]

        def r(text: str) -> str:
            return render_template(text, event_name, event_date, event_city)

        return {
            "subject_line": r(variant["subject"])[:60],
            "email_body": r(variant["email"]),
            "sms_body": r(variant["sms"])[:160],
        }

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Parse JSON from a model response, tolerating code fences / prose."""
        text = raw.strip()
        if text.startswith("```"):
            # Strip ```json ... ``` fences
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                return json.loads(text[start:end + 1])
            raise
