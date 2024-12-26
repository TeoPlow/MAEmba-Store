from fastapi import APIRouter
from uuid import UUID
from http import HTTPStatus
from fastapi.responses import JSONResponse

from src.core.exceptions import SpecialException
from src.handlers.validate_auth import validate_auth_handler
from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler
from src.handlers.email_confirm import (confirm_email_handler,
                                        send_confirmation_email_handler)
from src.core.logging import log

from src.schemas.user_auth_schema import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
    SendConfirmationEmailRequest,
    SendConfirmationEmailResponse,
    ValidateAuthRequest
)

router = APIRouter()


@router.post(
    "/register",
    description="Регистрация пользователя",
    response_model=RegisterUserResponse,
    response_description="UUID зарегистрированного пользователя",
)
async def register(request: RegisterUserRequest):
    log.debug("Регистрирую пользователя")
    try:
        registered_user_id: UUID = user_register_handler(request.model_dump())
        return JSONResponse(
            content={"status": "success",
                     "data": {"user_id": str(registered_user_id)}},
            status_code=HTTPStatus.CREATED
        )
    except SpecialException as e:
        log.error(e)
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.post(
    "/login",
    description="Авторизация пользователя",
    response_model=LoginResponse,
    response_description="Токен авторизации и срок его действия",
)
async def login(request: LoginRequest):
    log.debug("Авторизую пользователя")
    try:
        token, token_expiry = user_login_handler(request.model_dump())
        return JSONResponse(
            content={"status": "success",
                     "data": {"token": str(token),
                              "token-expiry": token_expiry.total_seconds()}},
            status_code=HTTPStatus.OK
        )
    except SpecialException as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.UNAUTHORIZED
        )
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.post(
    "/validate-auth",
    description="Проверка аутентификации пользователя",
)
async def validate_auth(request: ValidateAuthRequest):
    log.debug("Проверяю, аутентифицирован ли пользователь")
    try:
        validate_auth_handler(request)
        return JSONResponse(content={"status": "success"},
                            status_code=HTTPStatus.OK)
    except SpecialException as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.UNAUTHORIZED
        )
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.post(
    "/send-confirmation-email",
    description="Отправка ссылки на подтверждение почты",
    response_model=SendConfirmationEmailResponse,
    response_description="Сообщение об отправке письма",
)
async def send_confirmation_email(request: SendConfirmationEmailRequest):
    log.debug("Отправляю ссылку на подтверждение почты")
    try:
        message, fm = send_confirmation_email_handler(request.email,
                                                      request.user_id)
        await fm.send_message(message)
        return JSONResponse(
            content={"status": "success",
                     "message": "Письмо отправлено, проверьте почту."},
            status_code=HTTPStatus.OK
        )
    except SpecialException as e:
        log.error(e)
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.get(
    "/confirm-email/{token}",
    description="Подтверждение почты",
)
async def confirm_email(token: str):
    try:
        token_data = confirm_email_handler(token)
        return JSONResponse(
            content={"status": "success",
                     "message": f"Почта {token_data['email']} подтверждена"},
            status_code=HTTPStatus.OK
        )
    except SpecialException as e:
        log.error(e)
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


# @router.get("/protected-resource/")
# async def protected_resource(user_email: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_email).first()
#     if not user or not user.is_verified:
#         raise HTTPException(status_code=403,
#                             detail="Электронная почта не подтверждена")
#     return {"message": "Добро пожаловать в защищённый раздел!"}
