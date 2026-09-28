from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    name: str


class LocationUpdate(BaseModel):
    name: str | None = None


class LocationResponse(BaseModel):
    location_id: UUID
    user_id: UUID
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)