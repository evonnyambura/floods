from sqlalchemy.orm import Session

from app.models.sensor import Sensor


def create_sensor(db: Session, sensor: Sensor):
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


def get_sensor(db: Session, sensor_id):
    return db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()


def get_sensors(db: Session):
    return db.query(Sensor).all()


def update_sensor(db: Session, sensor: Sensor):
    db.commit()
    db.refresh(sensor)
    return sensor