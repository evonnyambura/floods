from sqlalchemy.orm import Session

from app.models.sensor_reading import SensorReading


def create_reading(db: Session, reading: SensorReading):
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


def get_reading(db: Session, reading_id):
    return db.query(SensorReading).filter(SensorReading.reading_id == reading_id).first()


def get_readings(db: Session):
    return db.query(SensorReading).all()


def get_sensor_readings(db: Session, sensor_id):
    return db.query(SensorReading).filter(SensorReading.sensor_id == sensor_id).all()