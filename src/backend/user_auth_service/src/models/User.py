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
    registration_date = Column(Date, nullable=True)
    legal_address = Column(String(255), nullable=True)
    physical_address = Column(String(255), nullable=True)
    inn = Column(String(12), nullable=True)
    ogrn = Column(String(13), nullable=True)
    kpp = Column(String(9), nullable=True)
    bik = Column(String(9), nullable=True)
    correspondent_account = Column(String(20), nullable=True)
    payment_account = Column(String(20), nullable=True)
    contact_number = Column(String(50), unique=True, nullable=False)
    user_role = Column(Enum(UserRoleEnum, create_type=False), nullable=False)
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
                contact_number: Optional[str],
                company_name: Optional[str]=None,
                company_type: Optional[str]=None, # Тип компании - ИП, ООО, АО, ЗАО
                director_name: Optional[str]=None, # ФИО директора
                registration_date: Optional[date]=None, # Дата регистрации - "YYYY-MM-DD"
                legal_address: Optional[str]=None, # Юридический адрес
                physical_address: Optional[str]=None,
                inn: Optional[int]=None, # 10 или 12 цифр
                ogrn: Optional[int]=None, # 13 цифр
                kpp: Optional[int]=None, # 9 цифр
                bik: Optional[int]=None, # 9 цифр
                correspondent_account: Optional[int]=None, # Корреспонденсткий счёт - 20 цифр 
                payment_account: Optional[int]=None # Расчётный счёт - 20 цифр
                ):
        self.user_type = self.check_user_type(user_type)
        self.username = self.check_username(username)
        self.email = self.check_email(email)
        self.password_hash = pbkdf2_sha256.hash(password)
        self.company_name = self.check_company_name(company_name)
        self.company_type = self.check_company_type(company_type)
        self.director_name = self.check_director_name(director_name)
        self.registration_date = self.check_registration_date(registration_date)
        self.legal_address = self.check_legal_address(legal_address)
        self.physical_address = self.check_physical_address(physical_address)
        self.inn = self.check_inn(inn)
        self.ogrn = self.check_ogrn(ogrn)
        self.kpp = self.check_kpp(kpp)
        self.bik = self.check_bik(bik)
        self.correspondent_account = self.check_correspondent_account(correspondent_account)
        self.payment_account = self.check_payment_account(payment_account)
        self.contact_number = self.check_contact_number(contact_number)
        self.user_role = UserRoleEnum.NotVerifyed
        
    
    def check_password(self, password: str) -> bool:
        result = pbkdf2_sha256.verify(password, self.password_hash)
        log.debug(f"Пароль проверен у {self.email}: {'success' if result else 'failure'}")
        return result
    
    def update_password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            log.warning(f"Ошибка при смене пароля у {self.email}: Неверный старый пароль")
            raise ValueError("Старый пароль не верен")
        self.password_hash = pbkdf2_sha256.hash(new_password)
        log.info(f"Пароль успешно сменён для {self.email}")


    def check_user_type(self, value: str):
        if value not in ["org", "ind"]:
            raise ValueError("Тип пользователя должно быть 'org' или 'ind'")
        return value

    def check_username(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Имя пользователя должно быть str")
        return value

    def check_email(self, value: str):
        if "@" not in value:
            raise ValueError("Неверный адрес почты")
        return value

    def check_company_name(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError("company_name должен быть str")
        return value

    def check_company_type(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError("company_type должен быть str")
        return value

    def check_director_name(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError("director_name должен быть str")
        return value

    def check_registration_date(self, value: Optional[date]):
        if not isinstance(value, Optional[date]):
            raise ValueError("registration_date должен быть date")
        return value

    def check_legal_address(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError("legal_address должен быть str")
        return value

    def check_physical_address(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError("physical_address должен быть str")
        return value

    def check_inn(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) not in (10, 12):
                raise ValueError("INN должен быть int с 10 или 12 цифрами")
        return value

    def check_ogrn(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) != 13:
                raise ValueError("ogrn должен быть int с 13 цифрами")
        return value

    def check_kpp(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) != 9:
                raise ValueError("kpp должен быть int с 9 цифрами")
        return value
    
    def check_bik(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) != 9:
                raise ValueError("bik должен быть int с 9 цифрами")
        return value

    def check_correspondent_account(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) != 20:
                raise ValueError("correspondent_account должен быть int с 20 цифрами")
        return value

    def check_payment_account(self, value: Optional[int]):
        if not isinstance(value, Optional[int]):
            if len(value) != 20:
                raise ValueError("payment_account должен быть int с 20 цифрами")
        return value

    def check_contact_number(self, value: Optional[str]):
        if not isinstance(value, Optional[str]):
            raise ValueError('contact_number должен быть str')
        return value
    
    
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
                "legal_adress": self.legal_address,
                "physical_adress": self.physical_address,
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
    
    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> "User":
        """
        Проверяет, соответствует ли словарь data требованиям класса.
        Создаёт объект, если всё верно, или вызывает исключение.
            Параметры:
                Словарь с данными для валидации.
                
            Возвращает:
                Объект User.
        """
        log.debug(f"Проверяю правильность введённых данных")
        try:
            if data["user_type"] == 'ind':
                return cls(
                    user_type=data["user_type"],
                    username=data["username"],
                    password=data["password"],
                    email=data["email"],
                    contact_number=data["contact_number"]
                )
            else:
                return cls(
                    user_type=data["user_type"],
                    username=data["username"],
                    password=data["password"],
                    email=data["email"],
                    contact_number=data["contact_number"],
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
                    payment_account=int(data["payment_account"])
                )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле: {e}")
        except ValueError as e:
            raise ValueError(f"Ошибка валидации данных: {e}")
        except Exception as e:
            raise ValueError(f"Неожиданная ошибка: {e}")
        
    def print_profile(self) -> str:
        if self.user_type == 'org':
            return (
                f"Тип пользователя: {self.user_type}\n"
                f"Имя пользователя: {self.username}\n"
                f"Контактный номер: {self.contact_number}\n"
                f"Email: {self.email}\n"
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
            )
        else:
            return (
                f"Тип пользователя: {self.user_type}\n"
                f"Имя пользователя: {self.username}\n"
                f"Email: {self.email}\n"
                f"Контактный номер: {self.contact_number}"
            )