from core.poi import get_top_pois_france
def generate_itinerary(city: str, days: int, trip_type: str) -> dict:
    # Берём реальные места (10 штук)
    pois = get_top_pois_france(city, trip_type, top_n=10)

    itinerary = []
    poi_idx = 0

    for day in range(1, days + 1):
        # по 3 места в день (утро/день/вечер), если не хватает — "Free time"
        def next_poi_name():
            nonlocal poi_idx
            if poi_idx >= len(pois):
                return "Free time"
            name = pois[poi_idx]["name"]
            poi_idx += 1
            return name

        itinerary.append({
            "day": day,
            "morning": next_poi_name(),
            "afternoon": next_poi_name(),
            "evening": next_poi_name(),
        })

    return {
        "city": city,
        "days": days,
        "trip_type": trip_type,
        "top_pois": [p["name"] for p in pois],
        "itinerary": itinerary,
        "data_sources": ["OpenStreetMap Nominatim", "OpenStreetMap Overpass"],
    }


def suggest_activity(time_of_day: str, trip_type: str) -> str:
    suggestions = {
        "calm": {
            "morning": "Relaxed breakfast and walk in a quiet area",
            "afternoon": "Museum or gallery visit",
            "evening": "Dinner in a calm local restaurant",
        },
        "active": {
            "morning": "Walking tour or bike ride",
            "afternoon": "Exploring main attractions",
            "evening": "Evening city walk",
        },
        "mixed": {
            "morning": "Coffee and short city walk",
            "afternoon": "Main attraction or museum",
            "evening": "Leisure walk or local food",
        },
        "city": {
            "morning": "Historic city center walk",
            "afternoon": "Museum or landmark visit",
            "evening": "Dinner in city center",
        },
        "nature": {
            "morning": "Park or nature walk",
            "afternoon": "Outdoor activity",
            "evening": "Relaxation with nature views",
        },
        "beach": {
            "morning": "Beach time",
            "afternoon": "Swimming or seaside walk",
            "evening": "Sunset near the sea",
        },
    }

    return suggestions.get(trip_type, {}).get(
        time_of_day, "Free time"
    )
