class IndividualProfile:
    def __init__(self, 
                first_name: str = None, 
                last_name: str = None, 
                email: str = None,
                phone_number: int = None):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
    @property
    def first_name(self) -> str:
        return self.__first_name
    @first_name.setter
    def first_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("first_name должно быть str")
        self.__first_name = value
    @property
    def last_name(self) -> str:
        return self.__last_name
    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("last_name должно быть str")
        self.__last_name = value
    @property
    def email(self) -> str:
        return self.__email
    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Неверный адрес почты")
        self.__email = value
    @property
    def phone_number(self) -> str:
        return self.__phone_number
    @phone_number.setter
    def phone_number(self, value: str):
        if not isinstance(value, str) or value[1:].isdigit() or len(value) > 17:
            raise ValueError("Не похоже на номер телефона")
        self.__phone_number = value
    def print_profile(self):
        return (f"Имя: {self.first_name}\n"
                f"Фамилия: {self.last_name}\n"
                f"Email: {self.email}\n"
                f"Номер телефона: {self.phone_number}")
    
