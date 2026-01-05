from fastapi import FastAPI
from core.itinerary import generate_itinerary

app = FastAPI(title="TripPlannerLite MVP")

@app.get("/")
def root():
    return {"status": "ok", "message": "TripPlannerLite API is running"}

@app.get("/itinerary")
def itinerary(city: str, days: int = 3, trip_type: str = "city"):
    return generate_itinerary(city, days, trip_type)
