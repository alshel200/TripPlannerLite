from fastapi import FastAPI

app = FastAPI(title="TripPlannerLite MVP")

@app.get("/")
def root():
    return {"status": "ok", "message": "TripPlannerLite API is running"}
