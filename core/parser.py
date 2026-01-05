import re
from datetime import datetime, date

ALLOWED_TYPES = {"city", "nature", "beach", "calm", "active", "mixed"}

def parse_request(text: str) -> dict:
    """
    Expected formats (examples):
    - Prague 29.03.2025-03.04.2025 mixed
    - Paris 17.12.2025-21.12.2025 city

    Returns dict with: city, start_date, end_date, trip_type, days
    """
    raw = (text or "").strip()

    # city can contain spaces, so we parse from the end:
    # <city> <dd.mm.yyyy>-<dd.mm.yyyy> <type>
    pattern = r"^(?P<city>.+?)\s+(?P<start>\d{2}\.\d{2}\.\d{4})-(?P<end>\d{2}\.\d{2}\.\d{4})\s+(?P<type>\w+)$"
    m = re.match(pattern, raw)
    if not m:
        raise ValueError("Wrong format. Use: City DD.MM.YYYY-DD.MM.YYYY trip_type")

    city = m.group("city").strip()
    trip_type = m.group("type").strip().lower()

    if trip_type not in ALLOWED_TYPES:
        raise ValueError(f"Unknown trip_type '{trip_type}'. Allowed: {', '.join(sorted(ALLOWED_TYPES))}")

    start = datetime.strptime(m.group("start"), "%d.%m.%Y").date()
    end = datetime.strptime(m.group("end"), "%d.%m.%Y").date()

    if end < start:
        raise ValueError("End date must be after start date")

    days = (end - start).days + 1  # inclusive

    # MVP limit
    if days > 5:
        raise ValueError("MVP limit: maximum 5 days. Please choose a shorter range.")

    return {
        "city": city,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "trip_type": trip_type,
        "days": days,
    }
def allowed_types_str() -> str:
    return ", ".join(sorted(ALLOWED_TYPES))
