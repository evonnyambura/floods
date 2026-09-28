from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.user import User
from app.repositories.location import create_location as create_location_repo, get_location as get_location_repo, get_locations as get_locations_repo, update_location as update_location_repo
from app.schemas.location import LocationCreate, LocationUpdate


def create_location(db: Session, location_data: LocationCreate, current_user: User):
    location = Location(user_id=current_user.user_id, name=location_data.name)
    return create_location_repo(db, location)


def get_location(db: Session, location_id: UUID):
    location = get_location_repo(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


def get_locations(db: Session):
    return get_locations_repo(db)


def update_location(db: Session, location_id: UUID, location_data: LocationUpdate):
    location = get_location_repo(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    updates = location_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(location, field, value)

    return update_location_repo(db, location)


def deactivate_location(db: Session, location_id: UUID):
    location = get_location_repo(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    location.is_active = False
    return update_location_repo(db, location)