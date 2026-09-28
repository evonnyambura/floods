from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.sensor import SensorStatus


class SensorCreate(BaseModel):
    location_id: UUID
    latitude: float
    longitude: float


class SensorUpdate(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class SensorResponse(BaseModel):
    sensor_id: UUID
    location_id: UUID
    latitude: float
    longitude: float
    status: SensorStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)