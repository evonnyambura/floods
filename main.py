from fastapi import FastAPI

from database import Base, engine
from app.models.user import User
from app.models.location import Location
from app.models.sensor import Sensor
from app.models.sensor_reading import SensorReading
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.location import router as location_router
from app.routers.sensor import router as sensor_router
from app.routers.sensor_reading import router as sensor_reading_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flood API", version="1.0.0")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(location_router)
app.include_router(sensor_router)
app.include_router(sensor_reading_router)


@app.get("/")
def root():
    return {"message": "Flood Monitoring API is running"}