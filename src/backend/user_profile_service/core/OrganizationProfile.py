from typing import List
from datetime import date
class OrganizationProfile:
    def __init__(self,
                email: str,
                company_name: str,
                company_type: str, # Тип компании - ИП, ООО, АО, ЗАО
                director_name: str, # ФИО директора
                registration_date: date, # Дата регистрации - "YYYY-MM-DD"
                legal_address: str, # Юридический адрес
                physical_address: str,
                inn: int, # 10 или 12 цифр
                ogrn: int, # 13 цифр
                kpp: int, # 9 цифр
                bik: int, # 9 цифр
                correspondent_account: int, # Корреспонденсткий счёт - 20 цифр 
                payment_account: int, # Расчётный счёт - 20 цифр
                contact_numbers: List[str]):
        self.__email = email
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
        self.__contact_numbers = contact_numbers
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
    def contact_numbers(self) -> List[str]:
        return self.__contact_numbers
    @contact_numbers.setter
    def contact_numbers(self, value: list):
        if not isinstance(value, list):
            raise ValueError('contact_numbers должен быть List[str]')
        for number in value:
            if isinstance(number, str) or len(number) > 17:
                raise ValueError(f"Не похож на номер телефон элемент {number}")
        self.__contact_numbers = value
    def print_profile(self) -> str:
        return (
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
            f"Email: {self.__email}\n"
            f"Контактные номера: {', '.join(self.__contact_numbers)}"
        )