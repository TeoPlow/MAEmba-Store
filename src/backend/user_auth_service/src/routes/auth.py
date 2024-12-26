from fastapi import Request, APIRouter
from uuid import UUID

from src.core.exceptions import SpecialException
from src.handlers.validate_auth import validate_auth_handler
from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler
from src.handlers.email_confirm import (confirm_email_handler,
                                        send_confirmation_email_handler)
from src.core.logging import log

router = APIRouter()


@router.post("/register")
async def register(request: Request):
    """
    Эндпоинт регистрации пользователя.
        На вход:
            Cловарь из class User в формате json.
            Пример:
                "Content-Type: application/json"
                {
                "user_type": "ind",
                "username": "egor228",
                "password": "password",
                "email": "citymodz@yandex.com",
                "contact_number": "+79853553825"
                }

        Возвращает:
            UUID зарегестрированного пользователя
            Пример:
            {
             "status": "success",
             "data": {"user_id": "eeee1234-76a9-4509-87f0-e1b12354d92b"}
            }
    """
    log.debug("Регистрирую пользователя")
    data = await request.json()
    registered_user_id: UUID = user_register_handler(data)
    return {"status": "success", "data": {"user_id": registered_user_id}}


@router.post("/login")
async def login(request: Request):
    """
    Эндпоинт авторизации пользователя.
        На вход:
            Cловарь из email_or_name: (str),
                       password: (str),
                       remember_me: (bool)
                       в формате json.
            Пример:
                "Content-Type: application/json"
                {
                "email_or_name": "username",
                "password": "pass12345",
                "remember_me": True
                }

        Возвращает:
            UUID Токен авторизации по ключу "token"
            Пример:
            {
             "status": "success",
             "data": {
                      "token": "eeee1234-76a9-4509-87f0-e1b12354d92b",
                      "token-expiry": 2592000.0
                     }
            }
    """
    log.debug("Авторизую пользователя")
    data = await request.json()
    # log.debug(f"Получил вот такой запрос: {data}")
    token, token_expiry = user_login_handler(data)
    return {"status": "success",
            "data": {"token": token, "token-expiry": token_expiry}}


@router.post("/validate-auth")
async def validate_auth(request: Request):
    """
    Эндпоинт проверки аутентификации пользователя, лутая токен из куки.
        На вход:
            Cловарь из auth_token: UUID
            Пример:
                "Content-Type: application/json"
                {
                "auth_token": "eeee1234-76a9-4509-87f0-e1b12354d92b",
                }
    """
    log.debug("Проверяю, аутентифицирован ли пользователь")
    try:
        data = await request.json()
        validate_auth_handler(data)
        return {"status": "success"}
    except SpecialException as e:
        log.error(f'Ошибка: {e}')
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.post("/send-confirmation-email")
async def send_confirmation_email(request: Request):
    """
    Эндпоинт отправки пользователю ссылки для авторизации почты.
        На вход:
            Cловарь из email: str,
                       user_id: UUID
            Пример:
                "Content-Type: application/json"
                {
                "email": "EvgenCumzoner@mail.ru",
                "user_id": eeee1234-76a9-4509-87f0-e1b12354d92b
                }
    """
    log.debug("Отправляю ссылку на подтверждение почты")
    try:
        data = await request.json()
        email, user_id = data["email"], data["user_id"]
        message, fm = send_confirmation_email_handler(email, user_id)

        await fm.send_message(message)
        return {"status": "success",
                "message": "Письмо отправлено, проверьте почту."}
    except SpecialException as e:
        log.error(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/confirm-email/{token}")
async def confirm_email(token: str):
    try:
        token_data = confirm_email_handler(token)
        return {"status": "success",
                "message": f"Почта {token_data['email']} успешно подтверждена"}
    except SpecialException as e:
        log.error(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


# @router.get("/protected-resource/")
# async def protected_resource(user_email: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_email).first()
#     if not user or not user.is_verified:
#         raise HTTPException(status_code=403,
#                             detail="Электронная почта не подтверждена")
#     return {"message": "Добро пожаловать в защищённый раздел!"}
