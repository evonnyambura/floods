from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sensor_reading import ReadingSeverity, SensorReading
from app.repositories.sensor_reading import (
    create_reading as create_reading_repo,
    get_reading as get_reading_repo,
    get_readings as get_readings_repo,
    get_sensor_readings as get_sensor_readings_repo
)
from app.schemas.sensor_reading import SensorReadingCreate


def calculate_severity(water_level: float) -> ReadingSeverity:
    if water_level < 20:
        return ReadingSeverity.LOW
    if water_level <= 40:
        return ReadingSeverity.MEDIUM
    return ReadingSeverity.HIGH


def create_reading(db: Session, reading_data: SensorReadingCreate):
    reading = SensorReading(
        sensor_id=reading_data.sensor_id,
        water_level=reading_data.water_level,
        severity=calculate_severity(reading_data.water_level)
    )
    return create_reading_repo(db, reading)


def get_reading(db: Session, reading_id: UUID):
    reading = get_reading_repo(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return reading


def get_readings(db: Session):
    return get_readings_repo(db)


def get_sensor_readings(db: Session, sensor_id: UUID):
    return get_sensor_readings_repo(db, sensor_id)