from typing import Any
import requests
from requests.exceptions import RequestException
from schemas.User import User
from core.exceptions import SpecialException
from core.logging import log

def put_user_info_handler(data: dict[str, Any]):
    """
    Добавляет информацию о пользователе в user_database.
        Параметры:
            Словарь вида:
                "user_type": "ind"
                "user_id": "UUID"
                "username": "string"
                "email": "string"
                "phone_number": "string"

                или

                "user_type": "org"
                "username": "string"
                "email": "string",
                "company_name": "string",
                "company_type": "string",
                "director_name": "string",
                "registration_date": "YYYY-MM-DD",
                "legal_address": "string",
                "physical_address": "string",
                "inn": 1234567890 (int),
                "ogrn": 1234567890123 (int),
                "kpp": 123456789 (int),
                "bik": 123456789 (int),
                "correspondent_account": 12345678901234567890 (int),
                "payment_account": 12345678901234567890 (int),
                "contact_numbers": "string"
    """