from sqlalchemy.orm import Session

from app.models.location import Location


def create_location(db: Session, location: Location):
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def get_location(db: Session, location_id):
    return db.query(Location).filter(Location.location_id == location_id).first()


def get_locations(db: Session):
    return db.query(Location).all()


def update_location(db: Session, location: Location):
    db.commit()
    db.refresh(location)
    return location