import requests
from fastapi import APIRouter, Request
from uuid import UUID

from src.core.config import USER_API_URL, RECAPTCHA_KEY
from src.core.exceptions import SpecialException
from src.core.auth import set_cookie, verify_recaptcha
# from src.core.auth import login_required, admin_required, same_user_required
from src.core.logging import log


router = APIRouter()

@router.get("/{user_id}")
async def get_user_info(user_id: UUID):
    log.debug("Получаю информацию о пользователе")
    url = USER_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.put("/{user_id}")
async def put_user_info(user_id: UUID, request: Request):
    log.debug("Добавляю информацию о пользователе")
    url = USER_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.post("/auth/register")
async def register(request: Request):
    log.debug("Регистрирую пользователя")
    url = USER_API_URL + f"/auth/register"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.post("/auth/login")
async def login(request: Request):
    log.debug("Авторизую уже существующего пользователя")
    url = USER_API_URL + f"/auth/login"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        if not verify_recaptcha(data["captcha_token"], RECAPTCHA_KEY):
            raise SpecialException("Капча не пройдена")

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "success":
            token = result["data"]["token"]
            token_expiry = result["data"]["token-expiry"]

            set_cookie(response,
                       "auth_token",
                       token,
                       max_age=token_expiry)
            log.debug(f"Установил ТОКЕН в куку")

        else:
            raise SpecialException(f"Ошибка при получении ответа: {result}")

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/auth/logout")
async def logout(request: Request):
    log.debug("Лишает пользователя авторизации")
    url = USER_API_URL + f"/auth/logout"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/auth/send-confirmation-email")
async def send_confirmation_email(request: Request):
    log.debug("Отправляю пользователю ссылку на почту для авторизации")
    url = USER_API_URL + f"/auth/send-confirmation-email"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/auth/confirm-email/{token}")
async def confirm_email(token: UUID):
    log.debug("Подтверждает почту по токену (из ссылки с почты)")
    url = USER_API_URL + f"/auth/confirm-email/{token}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/auth/validate-auth")
async def send_confirmation_email(request: Request):
    """
    Ничего на вход не принимает, он самостоятельный
    """
    log.debug("Проверяет аутентификацию пользователя по куке")
    url = USER_API_URL + f"/auth/validate-auth"
    headers = {"Content-Type": "application/json"}

    try:
        cookie_token: str = request.cookies.get("auth_token")
        if not cookie_token:
            raise SpecialException("Токен авторизации отсутствует")
        
        data = {"auth_token": cookie_token}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/auth/protected-resource/{user_id}")
async def confirm_email(user_id: UUID):
    log.debug("Предоставляет доступ к защищённому ресурсу")
    url = USER_API_URL + f"/auth/protected-resource/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/auth/change-password")
async def send_confirmation_email(request: Request):
    log.debug("Отправка ссылки на почту для изменения пароля")
    url = USER_API_URL + f"/auth/change-password"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/auth/confirm-change-password/{token}")
async def send_confirmation_email(request: Request, token: str):
    log.debug("Подтверждение изменения пароля по почте")
    url = USER_API_URL + f"/auth/confirm-change-password/{token}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от USER API: {result}")
        return result
    
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
