from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.sensor import create_sensor as create_sensor_repo, get_sensor as get_sensor_repo, get_sensors as get_sensors_repo, update_sensor as update_sensor_repo
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.models.sensor import Sensor, SensorStatus


def create_sensor(db: Session, sensor_data: SensorCreate):
    sensor = Sensor(location_id=sensor_data.location_id, latitude=sensor_data.latitude, longitude=sensor_data.longitude)
    return create_sensor_repo(db, sensor)


def get_sensor(db: Session, sensor_id: UUID):
    sensor = get_sensor_repo(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


def get_sensors(db: Session):
    return get_sensors_repo(db)


def update_sensor(db: Session, sensor_id: UUID, sensor_data: SensorUpdate):
    sensor = get_sensor_repo(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    updates = sensor_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(sensor, field, value)

    return update_sensor_repo(db, sensor)


def deactivate_sensor(db: Session, sensor_id: UUID):
    sensor = get_sensor_repo(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor.status = SensorStatus.INACTIVE
    return update_sensor_repo(db, sensor)