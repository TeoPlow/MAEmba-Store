from typing import Any, Dict, Optional
from pydantic import EmailStr
from datetime import date, datetime, timezone
from src.db.database import BaseUsers
from src.models.enum.UserRole import UserRoleEnum
from passlib.hash import pbkdf2_sha256
from uuid import uuid4

from sqlalchemy import (
    UUID,
    Column,
    Date,
    DateTime,
    Enum,
    String,
)

from src.core.logging import log


class User(BaseUsers):
    """
    Хранит в себе объект "Пользователя" который сразу может быть или Физ.Лицом или Юр.Лицом.
    """
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_type = Column(String(3), nullable=False)
    username = Column(String(255), nullable=False)
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
    phone_number = Column(String(50), unique=True, nullable=True)
    user_role = Column(Enum(UserRoleEnum), nullable=False)
    created = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def __init__(self,
                user_type: str, # 'org' или 'ind'
                username: str,
                password: str,
                email: EmailStr,
                company_name: Optional[str],
                company_type: Optional[str], # Тип компании - ИП, ООО, АО, ЗАО
                director_name: Optional[str], # ФИО директора
                registration_date: Optional[date], # Дата регистрации - "YYYY-MM-DD"
                legal_address: Optional[str], # Юридический адрес
                physical_address: Optional[str],
                inn: Optional[int], # 10 или 12 цифр
                ogrn: Optional[int], # 13 цифр
                kpp: Optional[int], # 9 цифр
                bik: Optional[int], # 9 цифр
                correspondent_account: Optional[int], # Корреспонденсткий счёт - 20 цифр 
                payment_account: Optional[int], # Расчётный счёт - 20 цифр
                contact_number: Optional[str]):
        self.user_type = user_type
        self.username = username
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)
        self.company_name = company_name
        self.company_type = company_type
        self.director_name = director_name
        self.registration_date = registration_date
        self.legal_address = legal_address
        self.physical_address = physical_address
        self.inn = inn
        self.ogrn = ogrn
        self.kpp = kpp
        self.bik = bik
        self.correspondent_account = correspondent_account
        self.payment_account = payment_account
        self.contact_number = contact_number
        log.info(f"Профиль пользователя {self.user_type} создан: {self.email}")
        
    
    def check_password(self, password: str) -> bool:
        result = pbkdf2_sha256.verify(password, self.password_hash)
        log.debug(f"Пароль проверен у {self.email}: {'success' if result else 'failure'}")
        return result
    
    @property
    def password(self) -> str:
        return self.password_hash
    
    @password.setter
    def password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            log.warning(f"Ошибка при смене пароля у {self.email}: Неверный старый пароль")
            raise ValueError("Старый пароль не верен")
        self.password_hash = pbkdf2_sha256.hash(new_password)
        log.info(f"Пароль успешно сменён для {self.email}")

    @property
    def user_type(self) -> str:
        return self.user_type
    
    @user_type.setter
    def user_type(self, value: str):
        if (value != "org") or (value != "ind"):
            raise ValueError("Тип пользователя должно быть 'org' или 'ind'")
        self.user_type = value
    
    @property
    def username(self) -> str:
        return self.username
    
    @username.setter
    def username(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Имя пользователя должно быть str")
        self.username = value

    @property
    def email(self) -> str:
        return self.email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Неверный адрес почты")
        self.email = value

    @property
    def company_name(self) -> str:
        return self.company_name

    @company_name.setter
    def company_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("company_name должен быть str")
        self.company_name = value

    @property
    def company_type(self) -> str:
        return self.company_type

    @company_type.setter
    def company_type(self, value: str):
        if not isinstance(value, str):
            raise ValueError("company_type должен быть str")
        self.company_type = value

    @property
    def director_name(self) -> str:
        return self.director_name

    @director_name.setter
    def director_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("director_name должен быть str")
        self.director_name = value

    @property
    def registration_date(self) -> date:
        return self.registration_date

    @registration_date.setter
    def registration_date(self, value: date):
        if not isinstance(value, date):
            raise ValueError("registration_date должен быть date")
        self.registration_date = value

    @property
    def legal_address(self) -> str:
        return self.legal_address

    @legal_address.setter
    def legal_address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("legal_address должен быть str")
        self.legal_address = value

    @property
    def physical_address(self) -> str:
        return self.physical_address

    @physical_address.setter
    def physical_address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("physical_address должен быть str")
        self.physical_address = value

    @property
    def inn(self) -> int:
        return self.inn

    @inn.setter
    def inn(self, value: int):
        if not isinstance(value, int) or len(value) not in (10, 12):
            raise ValueError("INN должен быть int с 10 или 12 цифрами")
        self.inn = value

    
    @property
    def ogrn(self) -> int:
        return self.ogrn

    @ogrn.setter
    def ogrn(self, value: int):
        if not isinstance(value, int) or len(value) == 13:
            raise ValueError("ogrn должен быть int с 13 цифрами")
        self.ogrn = value

    @property
    def kpp(self) -> int:
        return self.kpp

    @kpp.setter
    def kpp(self, value: int):
        if not isinstance(value, int) or len(value) == 9:
            raise ValueError("kpp должен быть int с 9 цифрами")
        self.kpp = value
    
    @property
    def bik(self) -> int:
        return self.bik

    @bik.setter
    def bik(self, value: int):
        if not isinstance(value, int) or len(value) == 9:
            raise ValueError("bik должен быть int с 9 цифрами")
        self.bik = value

    @property
    def correspondent_account(self) -> int:
        return self.correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: int):
        if not isinstance(value, int) or len(value) == 20:
            raise ValueError("correspondent_account должен быть int с 20 цифрами")
        self.correspondent_account = value

    @property
    def payment_account(self) -> int:
        return self.payment_account

    @payment_account.setter
    def payment_account(self, value: int):
        if not isinstance(value, int) or len(value) == 20:
            raise ValueError("payment_account должен быть int с 20 цифрами")
        self.payment_account = value

    @property
    def contact_number(self) -> str:
        return self.contact_number

    @contact_number.setter
    def contact_number(self, value: str):
        if not isinstance(value, str):
            raise ValueError('contact_number должен быть str')
        for number in value:
            if isinstance(number, str) or len(number) > 17:
                raise ValueError(f"Не похож на номер телефон элемент {number}")
        self.contact_number = value
    
    def to_dict(self) -> dict:
        log.debug(f"Конвертирую данные пользователя {self.email} в словарь")
        if self.user_type == 'ind':
            return {
                "id": str(self.id),
                "email": self.email,
                "user_type": self.user_type,
                "username": self.username,
                "contact_number": self.contact_number,
                "user_role": self.user_role.value,
                "created": self.created.isoformat(),
                "updated": self.updated.isoformat(),
            }
        else:
            return {
                "id": str(self.id),
                "email": self.email,
                "user_type": self.user_type,
                "username": self.username,
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
                "user_role": self.user_role.value,
                "created": self.created.isoformat(),
                "updated": self.updated.isoformat(),
            }
    
    def validate_data(cls, data: Dict[str, Any]) -> "User":
        """
        Проверяет, соответствует ли словарь data требованиям класса.
        Создаёт объект, если всё верно, или вызывает исключение.
            Параметры:
                Словарь с данными для валидации.
                
            Возвращает:
                Объект User.
        """
        try:
            if data["user_type"] == 'ind':
                return cls(
                    user_type=data["user_type"],
                    username=data["username"],
                    email=data["email"],
                    contact_number=data["contact_number"]
                )
            else:
                return cls(
                    user_type=data["user_type"],
                    username=data["username"],
                    email=data["email"],
                    company_name=data["company_name"],
                    company_type=data["company_type"],
                    director_name=data["director_name"],
                    registration_date=datetime.strptime(data["registration_date"], "%Y-%m-%d").date(),
                    legal_address=data["legal_address"],
                    physical_address=data["physical_address"],
                    inn=int(data["inn"]),
                    ogrn=int(data["ogrn"]),
                    kpp=int(data["kpp"]),
                    bik=int(data["bik"]),
                    correspondent_account=int(data["correspondent_account"]),
                    payment_account=int(data["payment_account"]),
                    contact_number=data["contact_number"]
                )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле: {e}")
        except ValueError as e:
            raise ValueError(f"Ошибка валидации данных: {e}")
        except Exception as e:
            raise ValueError(f"Неожиданная ошибка: {e}")
        
    def print_profile(self) -> str:
        if self.user_type == 'ind':
            return (
                f"Тип пользователя: {self.user_type}\n"
                f"Имя пользователя: {self.username}\n"
                f"Название компании: {self.company_name}\n"
                f"Тип компании: {self.company_type}\n"
                f"ФИО директора: {self.director_name}\n"
                f"Дата регистрации: {self.registration_date}\n"
                f"Юридический адрес: {self.legal_address}\n"
                f"Физический адрес: {self.physical_address}\n"
                f"ИНН: {self.inn}\n"
                f"ОГРН: {self.ogrn}\n"
                f"КПП: {self.kpp}\n"
                f"БИК: {self.bik}\n"
                f"Корреспонденсткий счёт: {self.correspondent_account}\n"
                f"Расчётный счёт: {self.payment_account}\n"
                f"Email: {self.email}\n"
                f"Контактный номер: {self.contact_number}"
            )
        else:
            return (
                f"Тип пользователя: {self.user_type}\n"
                f"Имя пользователя: {self.username}\n"
                f"Email: {self.email}\n"
                f"Контактный номер: {self.contact_number}"
            )