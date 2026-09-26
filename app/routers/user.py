from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserSelfUpdate,
    UserAdminUpdate,
    UserDisplayName,
)
from security import require_admin, get_current_user
from app.services.user import user_service

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return user_service.create(
        db,
        payload,
        current_user
    )

@router.get(
    "/",
    response_model=list[UserRead]
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    skip: int = 0,
    limit: int = 100,
):
    return user_service.get_all(
        db=db,
        skip=skip,
        limit=limit
    )

@router.get(
    "/me",
    response_model=UserRead
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.patch(
    "/me",
    response_model=UserRead
)
def update_my_profile(
    payload: UserSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_self(
        db,
        current_user,
        payload
    )

@router.get(
    "/directory/names",
    response_model=list[UserDisplayName]
)
def list_user_names(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 500,
):
    return user_service.get_all(
        db=db,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{user_id}",
    response_model=UserRead
)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return user_service.get(
        db,
        user_id
    )

@router.patch(
    "/{user_id}",
    response_model=UserRead
)
def update_user(
    user_id: UUID,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return user_service.update_admin(
        db,
        user_id,
        payload,
        current_user
    )

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserRead
)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return user_service.deactivate_user(
        db,
        user_id,
        current_user
    )
