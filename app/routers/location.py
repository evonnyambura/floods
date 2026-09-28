from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.models.user import User
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from security import require_admin
from app.services.location import create_location, get_location, get_locations, update_location, deactivate_location


router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/", response_model=LocationResponse)
def create(location: LocationCreate, db: Session = Depends(get_db)):
    return create_location(db, location)


@router.get("/", response_model=list[LocationResponse])
def get_all(db: Session = Depends(get_db)):
    return get_locations(db)


@router.get("/{location_id}", response_model=LocationResponse)
def get_one(location_id: UUID, db: Session = Depends(get_db)):
    return get_location(db, location_id)


@router.patch("/{location_id}", response_model=LocationResponse)
def update(
    location_id: UUID,
    location: LocationUpdate,
    db: Session = Depends(get_db)
):
    return update_location(db, location_id, location)


@router.patch("/{location_id}/deactivate", response_model=LocationResponse)
def deactivate(
    location_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return deactivate_location(db, location_id)