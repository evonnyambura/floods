from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self):
        self.model = User

    def get(
        self,
        db: Session,
        user_id: UUID
    ) -> User | None:
        return db.get(self.model, user_id)

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:
        result = db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:
        result = db.execute(
            select(self.model)
            .where(self.model.email == email)
        )

        return result.scalars().first()

    def create(
        self,
        db: Session,
        user: User
    ) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def update(
        self,
        db: Session,
        user: User
    ) -> User:
        db.commit()
        db.refresh(user)

        return user

    def deactivate(
        self,
        db: Session,
        user_id: UUID
    ) -> User | None:
        user = db.get(self.model, user_id)

        if user:
            user.is_active = False
            db.commit()
            db.refresh(user)

        return user


user_repository = UserRepository()