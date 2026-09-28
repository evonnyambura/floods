from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.models.user import User
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorResponse
from security import require_admin
from app.services.sensor import create_sensor, get_sensor, get_sensors, update_sensor, deactivate_sensor

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorResponse)
def create(sensor: SensorCreate, db: Session = Depends(get_db)):
    return create_sensor(db, sensor)


@router.get("/", response_model=list[SensorResponse])
def get_all(db: Session = Depends(get_db)):
    return get_sensors(db)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_one(sensor_id: UUID, db: Session = Depends(get_db)):
    return get_sensor(db, sensor_id)


@router.patch("/{sensor_id}", response_model=SensorResponse)
def update(sensor_id: UUID, sensor: SensorUpdate, db: Session = Depends(get_db)):
    return update_sensor(db, sensor_id, sensor)


@router.patch("/{sensor_id}/deactivate", response_model=SensorResponse)
def deactivate(sensor_id: UUID, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return deactivate_sensor(db, sensor_id)