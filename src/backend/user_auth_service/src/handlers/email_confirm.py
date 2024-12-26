import hashlib
import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from uuid import UUID, uuid4

from src.handlers.put_user_info import put_user_info_handler
from src.core.exceptions import SpecialException
from src.core.logging import log
from src.core.config import (MAIL_SERVER,
                             MAIL_PORT,
                             MAIL_USERNAME,
                             MAIL_PASSWORD,
                             MAIL_FROM,
                             MAIL_STARTTLS,
                             MAIL_SSL_TLS)


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)

user_tokens = {}


def generate_token(email: str, user_id: UUID) -> str:
    log.debug("Генирирую токен и сую его в user_tokens")
    token = hashlib.sha256(f"{email}{uuid4()}".encode()).hexdigest()
    expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
    user_tokens[token] = {"user_id": user_id, "email": email, "expiry": expiry}
    return token


def send_confirmation_email_handler(email: str, user_id: UUID):
    log.debug(f"Отправляю пользователю {email} ссылку на подтверждение почты")
    token = generate_token(email, user_id)
    log.debug(f"user_tokens: {user_tokens}")
    confirmation_url = f"http://localhost:8000/auth/confirm-email/{token}"

    message = MessageSchema(
        subject="Подтверждение вашей электронной почты",
        recipients=[email],
        body=f"Перейдите по ссылке для подтверждения: {confirmation_url}",
        subtype="plain"
    )

    fm = FastMail(conf)
    # log.debug(f"Вот с такого конфига отправляется запрос:\n {conf}")
    return message, fm


def confirm_email_handler(token):
    log.debug("Подтверждаю почту пользователя")
    token_data = user_tokens.get(token)

    if not token_data:
        raise SpecialException("Неверный токен")
    if token_data["expiry"] < datetime.datetime.now():
        raise SpecialException("Токен истёк")

    put_user_info_handler(token_data["user_id"], {"user_role": "Verifyed"})

    del user_tokens[token]
    return token_data
