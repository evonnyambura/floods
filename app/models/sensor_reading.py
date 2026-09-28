from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class ReadingSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    reading_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.sensor_id"), nullable=False)
    water_level = Column(Float, nullable=False)
    severity = Column(SQLEnum(ReadingSeverity), nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)