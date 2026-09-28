from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.sensor_reading import ReadingSeverity


class SensorReadingCreate(BaseModel):
    sensor_id: UUID
    water_level: float


class SensorReadingResponse(BaseModel):
    reading_id: UUID
    sensor_id: UUID
    water_level: float
    severity: ReadingSeverity
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)