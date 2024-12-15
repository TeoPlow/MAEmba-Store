from typing import Any, Dict, Optional
from pydantic import EmailStr
from datetime import date, datetime
from passlib.hash import pbkdf2_sha256
from src.core.logging import log


class User():
    """
    Хранит в себе объект "Пользователя" который сразу может быть или Физ.Лицом или Юр.Лицом.
    """
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
        self.__user_type = user_type
        self.__username = username
        self.__email = email
        self.__password_hash = pbkdf2_sha256.hash(password)
        self.__company_name = company_name
        self.__company_type = company_type
        self.__director_name = director_name
        self.__registration_date = registration_date
        self.__legal_address = legal_address
        self.__physical_address = physical_address
        self.__inn = inn
        self.__ogrn = ogrn
        self.__kpp = kpp
        self.__bik = bik
        self.__correspondent_account = correspondent_account
        self.__payment_account = payment_account
        self.__contact_number = contact_number
        
    
    def check_password(self, password: str) -> bool:
        result = pbkdf2_sha256.verify(password, self.__password_hash)
        log.debug(f"Пароль проверен у {self.__email}: {'success' if result else 'failure'}")
        return result
    
    @property
    def password(self) -> str:
        return self.__password_hash
    
    @password.setter
    def password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            log.warning(f"Ошибка при смене пароля у {self.__email}: Неверный старый пароль")
            raise ValueError("Старый пароль не верен")
        self.__password_hash = pbkdf2_sha256.hash(new_password)
        log.info(f"Пароль успешно сменён для {self.__email}")

    @property
    def user_type(self) -> str:
        return self.__user_type
    
    @user_type.setter
    def user_type(self, value: str):
        if (value != "org") and (value != "ind"):
            raise ValueError("Тип пользователя должно быть 'org' или 'ind'")
        self.__user_type = value
    
    @property
    def username(self) -> str:
        return self.__username
    
    @username.setter
    def username(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Имя пользователя должно быть str")
        self.__username = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Неверный адрес почты")
        self.__email = value

    @property
    def company_name(self) -> str:
        return self.__company_name

    @company_name.setter
    def company_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("company_name должен быть str")
        self.__company_name = value

    @property
    def company_type(self) -> str:
        return self.__company_type

    @company_type.setter
    def company_type(self, value: str):
        if not isinstance(value, str):
            raise ValueError("company_type должен быть str")
        self.__company_type = value

    @property
    def director_name(self) -> str:
        return self.__director_name

    @director_name.setter
    def director_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("director_name должен быть str")
        self.__director_name = value

    @property
    def registration_date(self) -> date:
        return self.__registration_date

    @registration_date.setter
    def registration_date(self, value: date):
        if not isinstance(value, date):
            raise ValueError("registration_date должен быть date")
        self.__registration_date = value

    @property
    def legal_address(self) -> str:
        return self.__legal_address

    @legal_address.setter
    def legal_address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("legal_address должен быть str")
        self.__legal_address = value

    @property
    def physical_address(self) -> str:
        return self.__physical_address

    @physical_address.setter
    def physical_address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("physical_address должен быть str")
        self.__physical_address = value

    @property
    def inn(self) -> int:
        return self.__inn

    @inn.setter
    def inn(self, value: int):
        if not isinstance(value, int) or len(value) not in (10, 12):
            raise ValueError("INN должен быть int с 10 или 12 цифрами")
        self.__inn = value

    
    @property
    def ogrn(self) -> int:
        return self.__ogrn

    @ogrn.setter
    def ogrn(self, value: int):
        if not isinstance(value, int) or len(value) == 13:
            raise ValueError("ogrn должен быть int с 13 цифрами")
        self.__ogrn = value

    @property
    def kpp(self) -> int:
        return self.__kpp

    @kpp.setter
    def kpp(self, value: int):
        if not isinstance(value, int) or len(value) == 9:
            raise ValueError("kpp должен быть int с 9 цифрами")
        self.__kpp = value
    
    @property
    def bik(self) -> int:
        return self.__bik

    @bik.setter
    def bik(self, value: int):
        if not isinstance(value, int) or len(value) == 9:
            raise ValueError("bik должен быть int с 9 цифрами")
        self.__bik = value

    @property
    def correspondent_account(self) -> int:
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: int):
        if not isinstance(value, int) or len(value) == 20:
            raise ValueError("correspondent_account должен быть int с 20 цифрами")
        self.__correspondent_account = value

    @property
    def payment_account(self) -> int:
        return self.__payment_account

    @payment_account.setter
    def payment_account(self, value: int):
        if not isinstance(value, int) or len(value) == 20:
            raise ValueError("payment_account должен быть int с 20 цифрами")
        self.__payment_account = value

    @property
    def contact_number(self) -> str:
        return self.__contact_number

    @contact_number.setter
    def contact_number(self, value: str):
        if not isinstance(value, str):
            raise ValueError('contact_number должен быть str')
        for number in value:
            if isinstance(number, str) or len(number) > 17:
                raise ValueError(f"Не похож на номер телефон элемент {number}")
        self.__contact_number = value
    
    
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
        if self.user_type == 'ind':
            return (
                f"Тип пользователя: {self.__user_type}\n"
                f"Имя пользователя: {self.__username}\n"
                f"Контактный номер: {self.__contact_number}\n"
                f"Email: {self.__email}\n"
                f"Название компании: {self.__company_name}\n"
                f"Тип компании: {self.__company_type}\n"
                f"ФИО директора: {self.__director_name}\n"
                f"Дата регистрации: {self.__registration_date}\n"
                f"Юридический адрес: {self.__legal_address}\n"
                f"Физический адрес: {self.__physical_address}\n"
                f"ИНН: {self.__inn}\n"
                f"ОГРН: {self.__ogrn}\n"
                f"КПП: {self.__kpp}\n"
                f"БИК: {self.__bik}\n"
                f"Корреспонденсткий счёт: {self.__correspondent_account}\n"
                f"Расчётный счёт: {self.__payment_account}\n"
            )
        else:
            return (
                f"Тип пользователя: {self.__user_type}\n"
                f"Имя пользователя: {self.__username}\n"
                f"Email: {self.__email}\n"
                f"Контактный номер: {self.__contact_number}"
            )