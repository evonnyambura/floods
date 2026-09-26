from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import SetupAdminCreate, UserRead
from app.services.user import user_service
from security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/setup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def setup_admin(
    payload: SetupAdminCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_admin(
        db,
        payload
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    user = user_service.authenticate(
        db,
        payload.email,
        payload.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }