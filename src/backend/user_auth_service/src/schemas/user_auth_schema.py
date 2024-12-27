from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


# Общая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    user_type: str
    username: str
    password: str
    contact_number: Optional[str] = Field(None, description="Номер телефона")
    user_role: Optional[str] = Field(None, description="Роль пользователя")
    company_name: Optional[str] = Field(None, description="Название компании")
    company_type: Optional[str] = Field(None, description="Тип компании")
    director_name: Optional[str] = Field(None, description="Имя директора")
    legal_address: Optional[str] = Field(None, description="Юр.Адрес")
    physical_address: Optional[str] = Field(None,
                                            description="Физический адрес")
    inn: Optional[str] = Field(None, description="ИНН")
    ogrn: Optional[str] = Field(None, description="ОГРН")
    kpp: Optional[str] = Field(None, description="КПП")
    bik: Optional[str] = Field(None, description="БИК")
    correspondent_account: Optional[str] = Field(None,
                                                 description="Корресп. счёт")
    payment_account: Optional[str] = Field(None, description="Платёжный счёт")


# Схема для GET /{user_id}
class UserDto(UserBase):
    id: UUID
    created: datetime
    updated: datetime


# Схема для POST /register
class RegisterUserRequest(UserBase):
    password: str


class RegisterUserResponse(BaseModel):
    status: str
    data: dict[str, UUID] = Field(...,
                                  description="Содержит ID зарег. пользов.")


# Схема для POST /login
class LoginRequest(BaseModel):
    email_or_name: str
    password: str
    remember_me: bool = Field(False,
                              description="Запомнить пользователя")


class LoginResponse(BaseModel):
    status: str
    data: dict[str, str] = Field(
        ...,
        description="Содержит токен авторизации и его срок действия",
        example={"token": "eeee1234-76a9-4509-87f0-e1b12354d92b",
                 "token-expiry": "2592000.0"},
    )


class ValidateAuthRequest(BaseModel):
    auth_token: UUID


# Схема для POST /send-confirmation-email
class SendConfirmationEmailRequest(BaseModel):
    email: EmailStr
    user_id: UUID


class SendConfirmationEmailResponse(BaseModel):
    status: str
    message: str


# Схема для POST /change-password
class ChangePasswordRequest(BaseModel):
    email: EmailStr
    user_id: UUID


class ChangePasswordResponse(BaseModel):
    status: str
    message: str


# Схема для POST /confirm-change-password
class ConfirmChangePasswordRequest(BaseModel):
    user_id: UUID
    password: str


# Схема для POST /logout
class LogoutRequest(BaseModel):
    user_id: UUID
