from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


class LocationUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class LocationResponse(BaseModel):
    location_id: UUID
    name: str
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)