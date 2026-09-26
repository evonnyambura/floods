from __future__ import annotations

from uuid import UUID
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import (
    UserCreate,
    UserSelfUpdate,
    UserAdminUpdate,
    SetupAdminCreate,
)


class UserService:
    def __init__(self):
        self.repository = user_repository

    def get(
        self,
        db: Session,
        user_id: UUID
    ) -> User:
        user = self.repository.get(db, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:
        return self.repository.get_all(
            db,
            skip=skip,
            limit=limit
        )

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:
        return self.repository.get_by_email(
            db,
            email.lower()
        )

    def hash_password(
        self,
        password: str
    ) -> str:
        password_bytes = password.encode("utf-8")

        if len(password_bytes) > 72:
            raise ValueError(
                "Password cannot exceed 72 bytes"
            )

        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(
            password_bytes,
            salt
        )

        return hashed_bytes.decode("utf-8")

    def create(
        self,
        db: Session,
        payload: UserCreate,
        current_user: User
    ) -> User:

        existing_user = self.get_by_email(
            db,
            payload.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )

        hashed_password = self.hash_password(
            payload.password
        )

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email.lower(),
            role=payload.role,
            password_hash=hashed_password,
        )

        return self.repository.create(
            db,
            user
        )

    def create_admin(
        self,
        db: Session,
        payload: SetupAdminCreate
    ) -> User:
        

        if payload.email:
            existing_user = self.get_by_email(
                db,
                payload.email
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists."
                )

            admin_email = payload.email.lower()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required for the administrator."
            )

        hashed_password = self.hash_password(
            payload.password
        )

        admin = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=admin_email,
            role="admin",
            password_hash=hashed_password,
        )

        return self.repository.create(
            db,
            admin
        )


    def update_self(
        self,
        db: Session,
        db_obj: User,
        payload: UserSelfUpdate
    ) -> User:

        data = payload.model_dump(
            exclude_unset=True
        )

        password = data.get("password")

        if password:
            db_obj.password_hash = self.hash_password(
                password
            )

        data.pop("password", None)
        data.pop("confirm_password", None)

        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update_admin(
        self,
        db: Session,
        user_id: UUID,
        payload: UserAdminUpdate,
        current_user: User
    ) -> User:

        db_obj = self.get(
            db,
            user_id
        )

        data = payload.model_dump(
            exclude_unset=True
        )

        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def authenticate(
        self,
        db: Session,
        email: str,
        password_plain: str
    ) -> User | None:

        user = self.repository.get_by_email(
            db,
            email.lower()
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if (
            user.locked_until
            and user.locked_until > datetime.now(timezone.utc)
        ):
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=(
                    "Account temporarily locked due to "
                    "too many failed login attempts. "
                    "Try again later."
                )
            )

        password_bytes = password_plain.encode("utf-8")

        if len(password_bytes) > 72:
            return None

        hash_bytes = user.password_hash.encode("utf-8")

        if not bcrypt.checkpw(
            password_bytes,
            hash_bytes
        ):
            user.failed_attempts += 1

            if user.failed_attempts >= 3:
                user.locked_until = (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=15)
                )

            db.commit()

            return None

        user.failed_attempts = 0
        user.locked_until = None

        db.commit()

        return user

    def deactivate_user(
        self,
        db: Session,
        user_id: UUID,
        current_user: User
    ) -> User:

        user = self.repository.deactivate(
            db,
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user


user_service = UserService()