import logging
import datetime

from typing import Optional, Self
from uuid import uuid4

from passlib.hash import pbkdf2_sha256
from pydantic import EmailStr

from src.models.enum.UserRole import UserRoleEnum

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)

from src.db.database import BaseUsers

# Настройка логгера
logger = logging.getLogger("models.individual_profile")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class IndividualProfile(BaseUsers):
    __tablename__ = "individual_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone_number = Column(String(50), unique=True, nullable=True)
    user_role = Column(Enum(UserRoleEnum), nullable=False)
    created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    def __init__(
        self,
        email: EmailStr,
        password: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        user_role: UserRoleEnum,
    ) -> None:
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.user_role = user_role
        logger.info(f"New user profile created: {self.email}")

    def check_password(self, password: str) -> bool:
        result = pbkdf2_sha256.verify(password, self.password_hash)
        logger.debug(f"Password check for {self.email}: {'success' if result else 'failure'}")
        return result

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            logger.warning(f"Failed password change for {self.email}: incorrect old password")
            raise ValueError("Old password is incorrect")
        self.password_hash = pbkdf2_sha256.hash(new_password)
        logger.info(f"Password changed for {self.email}")
    
    def update_email(self, email: str) -> Self:
        self.email = email if email else self.email
        return self
    
    def update_personal(
        self,
        email: Optional[EmailStr] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> Self:
        changes = []
        if email and email != self.email:
            self.email = email
            changes.append("email")
        if first_name and first_name != self.first_name:
            self.first_name = first_name
            changes.append("first_name")
        if last_name and last_name != self.last_name:
            self.last_name = last_name
            changes.append("last_name")
        if phone_number and phone_number != self.phone_number:
            self.phone_number = phone_number
            changes.append("phone_number")
        logger.info(f"Updated fields for {self.email}: {', '.join(changes)}")
        return self

    def to_dict(self) -> dict:
        logger.debug(f"Converting profile to dict: {self.email}")
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "user_role": self.user_role.value,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
        }