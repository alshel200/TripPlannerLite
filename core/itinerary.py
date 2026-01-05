def generate_itinerary(city: str, days: int, trip_type: str) -> dict:
    itinerary = []

    for day in range(1, days + 1):
        day_plan = {
            "day": day,
            "morning": suggest_activity("morning", trip_type),
            "afternoon": suggest_activity("afternoon", trip_type),
            "evening": suggest_activity("evening", trip_type),
        }
        itinerary.append(day_plan)

    return {
        "city": city,
        "days": days,
        "trip_type": trip_type,
        "itinerary": itinerary,
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
