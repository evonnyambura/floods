import enum
import uuid


from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Enum, String, Boolean, Integer
from sqlalchemy.sql import func

from database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        autoincrement=False,
        index=True
    )

    role = Column(
        Enum(UserRole),
        nullable=False
    )

    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        unique=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    locked_until = Column(
        DateTime(timezone=True), 
        nullable=True
    )
    
    failed_attempts = Column(
        Integer, 
        default=0, 
        nullable=False
    )

    def __repr__(self):
        return (
            f"<User(user_id={self.user_id}, "
            f"email={self.email}, "
            f"role={self.role})>"
        )