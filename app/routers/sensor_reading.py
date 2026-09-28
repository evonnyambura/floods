from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse
from app.services.sensor_reading import create_reading, get_reading, get_readings, get_sensor_readings

router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


@router.post("/", response_model=SensorReadingResponse)
def create(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    return create_reading(db, reading)


@router.get("/", response_model=list[SensorReadingResponse])
def get_all(db: Session = Depends(get_db)):
    return get_readings(db)


@router.get("/{reading_id}", response_model=SensorReadingResponse)
def get_one(reading_id: UUID, db: Session = Depends(get_db)):
    return get_reading(db, reading_id)


@router.get("/sensor/{sensor_id}", response_model=list[SensorReadingResponse])
def get_by_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    return get_sensor_readings(db, sensor_id)