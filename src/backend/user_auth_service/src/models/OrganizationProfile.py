import logging
import datetime

from typing import Optional, Self
from uuid import uuid4

from passlib.hash import pbkdf2_sha256
from pydantic import EmailStr

from src.models.enum.OrganizationRole import OrganizationRoleEnum

from sqlalchemy import (
    UUID,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)

from src.db.database import BaseUsers

# Настройка логгера
logger = logging.getLogger("models.organization_profile")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class OrganizationProfile(BaseUsers):
    __tablename__ = "organization_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    company_type = Column(String(50), nullable=True)
    director_name = Column(String(255), nullable=True)
    registration_date = Column(Date, nullable=False)
    legal_adress = Column(String(255), nullable=False)
    physical_adress = Column(String(255), nullable=False)
    inn = Column(String(12), nullable=False)
    ogrn = Column(String(13), nullable=False)
    kpp = Column(String(9), nullable=False)
    bik = Column(String(9), nullable=False)
    correspondent_account = Column(String(20), nullable=False)
    payment_account = Column(String(20), nullable=False)
    contact_number = Column(String(50), unique=True, nullable=True)
    organization_role = Column(Enum(OrganizationRoleEnum), nullable=False)
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
        company_name: str,
        company_type: str,
        director_name: str,
        registration_date: Date,
        legal_adress: str,
        physical_adress: str,
        inn: str,
        ogrn: str,
        kpp: str,
        bik: str,
        correspondent_account: str,
        payment_account: str,
        contact_number: str,
        organization_role: OrganizationRoleEnum,
    ) -> None:
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)
        self.company_name = company_name
        self.company_type = company_type
        self.director_name = director_name
        self.registration_date = registration_date
        self.legal_adress = legal_adress
        self.physical_adress = physical_adress
        self.inn = inn
        self.ogrn = ogrn
        self.kpp = kpp
        self.bik = bik
        self.correspondent_account = correspondent_account
        self.payment_account = payment_account
        self.contact_number = contact_number
        self.organization_role = organization_role
        logger.info(f"New organization profile created: {self.email}")

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
        company_name: Optional[str] = None,
        company_type: Optional[str] = None,
        director_name: Optional[str] = None,
        registration_date: Optional[Date] = None,
        legal_adress: Optional[str] = None,
        physical_adress: Optional[str] = None,
        inn: Optional[str] = None,
        ogrn: Optional[str] = None,
        kpp: Optional[str] = None,
        bik: Optional[str] = None,
        correspondent_account: Optional[str] = None,
        payment_account: Optional[str] = None,
        contact_number: Optional[str] = None,
    ) -> Self:
        changes = []
        if email and email != self.email:
            self.email = email
            changes.append("email")
        if company_name and company_name != self.company_name:
            self.company_name = company_name
            changes.append("company_name")
        if company_type and company_type != self.company_type:
            self.company_type = company_type
            changes.append("company_type")
        if director_name and director_name != self.director_name:
            self.director_name = director_name
            changes.append("director_name")
        if registration_date and registration_date != self.registration_date:
            self.registration_date = registration_date
            changes.append("registration_date")
        if legal_adress and legal_adress != self.legal_adress:
            self.legal_adress = legal_adress
            changes.append("legal_adress")
        if physical_adress and physical_adress != self.physical_adress:
            self.physical_adress = physical_adress
            changes.append("physical_adress")
        if inn and inn != self.inn:
            self.inn = inn
            changes.append("inn")
        if ogrn and ogrn != self.ogrn:
            self.ogrn = ogrn
            changes.append("ogrn")
        if kpp and kpp != self.kpp:
            self.kpp = kpp
            changes.append("kpp")
        if bik and bik != self.bik:
            self.bik = bik
            changes.append("bik")
        if correspondent_account and correspondent_account != self.correspondent_account:
            self.correspondent_account = correspondent_account
            changes.append("correspondent_account")
        if payment_account and payment_account != self.payment_account:
            self.payment_account = payment_account
            changes.append("payment_account")
        if contact_number and contact_number != self.contact_number:
            self.contact_number = contact_number
            changes.append("contact_number")
        logger.info(f"Updated fields for {self.email}: {', '.join(changes)}")
        return self

    def to_dict(self) -> dict:
        logger.debug(f"Converting organization profile to dict: {self.email}")
        return {
            "id": str(self.id),
            "email": self.email,
            "company_name": self.company_name,
            "company_type": self.company_type,
            "director_name": self.director_name,
            "registration_date": self.registration_date,
            "legal_adresslegal_adress": self.legal_adress,
            "physical_adress": self.physical_adress,
            "inn": self.inn,
            "ogrn": self.ogrn,
            "kpp": self.kpp,
            "bik": self.bik,
            "correspondent_account": self.correspondent_account,
            "payment_account": self.payment_account,
            "contact_number": self.contact_number,
            "organization_role": self.organization_role.value,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
        }