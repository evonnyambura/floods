from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)

from app.models.user import UserRole
from app.schemas.validators import sanitize_text_field, validate_strong_password


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole

    @field_validator("first_name")
    @classmethod
    def clean_first_name(cls, value: str) -> str:
        return sanitize_text_field(value, "First name")

    @field_validator("last_name")
    @classmethod
    def clean_last_name(cls, value: str) -> str:
        return sanitize_text_field(value, "Last name")


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        return validate_strong_password(value)

    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value


class UserSelfUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=72
    )
    confirm_password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=72
    )

    @field_validator("first_name")
    @classmethod
    def clean_first_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return sanitize_text_field(value, "First name")

    @field_validator("last_name")
    @classmethod
    def clean_last_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return sanitize_text_field(value, "Last name")

    @field_validator("password")
    @classmethod
    def check_password_strength(
        cls,
        value: Optional[str]
    ) -> Optional[str]:
        if value is None:
            return value
        return validate_strong_password(value)

    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(
        cls,
        value: Optional[str],
        info
    ) -> Optional[str]:
        if (
            "password" in info.data
            and info.data["password"] is not None
            and value != info.data["password"]
        ):
            raise ValueError("Passwords do not match")
        return value


class UserAdminUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    @field_validator("first_name")
    @classmethod
    def clean_first_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return sanitize_text_field(value, "First name")

    @field_validator("last_name")
    @classmethod
    def clean_last_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return sanitize_text_field(value, "Last name")


class UserRead(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class UserDisplayName(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class SetupAdminCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @field_validator("first_name")
    @classmethod
    def clean_first_name(cls, value: str) -> str:
        return sanitize_text_field(value, "First name")

    @field_validator("last_name")
    @classmethod
    def clean_last_name(cls, value: str) -> str:
        return sanitize_text_field(value, "Last name")

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        return validate_strong_password(value)

    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value