import time
import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Важно: указываем нормальный User-Agent (требование Nominatim policy)
HEADERS = {
    "User-Agent": "TripPlannerLiteMVP/1.0 (edu-project)"
}


# Простая карта "тип отдыха -> какие теги POI искать"
# Это MVP-логика: потом расширим.
TRIP_TYPE_TAGS = {
    "active": [
        ('leisure', 'sports_centre'),
        ('leisure', 'park'),
        ('tourism', 'viewpoint'),
        ('route', 'hiking'),  # чаще relation
    ],
    "calm": [
        ('tourism', 'museum'),
        ('tourism', 'gallery'),
        ('leisure', 'garden'),
        ('amenity', 'theatre'),
        ('amenity', 'library'),
    ],
    "mixed": [
        ('tourism', 'museum'),
        ('leisure', 'park'),
        ('tourism', 'attraction'),
        ('tourism', 'viewpoint'),
    ],
    # для совместимости с вашими типами:
    "city": [
        ('tourism', 'attraction'),
        ('tourism', 'museum'),
        ('historic', 'monument'),
        ('tourism', 'viewpoint'),
    ],
    "nature": [
        ('leisure', 'park'),
        ('leisure', 'nature_reserve'),
        ('tourism', 'viewpoint'),
    ],
    "beach": [
        ('natural', 'beach'),
        ('tourism', 'viewpoint'),
    ],
}

def geocode_city_france(city: str) -> tuple[float, float]:
    """
    Возвращает (lat, lon) для города во Франции через Nominatim.
    """
    # Важно: Nominatim public policy — не долбить запросами, в MVP делаем минимальный троттлинг.
    time.sleep(1.0)

    params = {
        "q": f"{city}, France",
        "format": "json",
        "limit": 1,
    }
    r = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    if not data:
        raise ValueError(f"City not found in France: {city}")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


def fetch_poi_overpass(lat: float, lon: float, tags: list[tuple[str, str]], radius_m: int = 5000, limit: int = 50) -> list[dict]:
    """
    Тянем POI вокруг координат. Берём nwr (node/way/relation) чтобы не потерять POI, которые размечены как way/relation.
    """
    # Собираем фильтры по тегам
    # Пример: nwr["tourism"="museum"](around:5000,lat,lon);
    tag_blocks = "\n".join(
        [f'nwr["{k}"="{v}"](around:{radius_m},{lat},{lon});' for k, v in tags]
    )

    query = f"""
    [out:json][timeout:25];
    (
      {tag_blocks}
    );
    out center tags;
    """

    r = requests.post(OVERPASS_URL, data=query.encode("utf-8"), headers=HEADERS, timeout=60)
    r.raise_for_status()
    data = r.json()

    elements = data.get("elements", [])

    # нормализуем в единый вид
    pois = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        # для way/relation координаты чаще в "center"
        if "lat" in el and "lon" in el:
            poi_lat, poi_lon = el["lat"], el["lon"]
        else:
            center = el.get("center") or {}
            poi_lat, poi_lon = center.get("lat"), center.get("lon")
            if poi_lat is None or poi_lon is None:
                continue

        pois.append({
            "name": name,
            "lat": poi_lat,
            "lon": poi_lon,
            "tags": tags,
        })

    # грубая дедупликация по имени
    seen = set()
    uniq = []
    for p in pois:
        key = p["name"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(p)

    return uniq[:limit]


def get_top_pois_france(city: str, trip_type: str, top_n: int = 10) -> list[dict]:
    tt = trip_type.lower()
    tags = TRIP_TYPE_TAGS.get(tt)
    if not tags:
        tags = TRIP_TYPE_TAGS["mixed"]

    lat, lon = geocode_city_france(city)
    pois = fetch_poi_overpass(lat, lon, tags=tags, radius_m=6000, limit=80)

    # если мало — расширяем выбор универсальными tourism=attraction
    if len(pois) < top_n:
        extra = fetch_poi_overpass(lat, lon, tags=[("tourism", "attraction")], radius_m=6000, limit=80)
        # добавляем, не дублируя по имени
        existing = {p["name"].strip().lower() for p in pois}
        for e in extra:
            k = e["name"].strip().lower()
            if k not in existing:
                pois.append(e)
                existing.add(k)
            if len(pois) >= top_n:
                break

    return pois[:top_n]
