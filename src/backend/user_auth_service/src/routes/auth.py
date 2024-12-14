from fastapi import APIRouter, Request
from uuid import UUID
from core.exceptions import SpecialException
from core.logging import log
from handlers.individual_register import individual_register_handler
# from handlers.organization_register import organization_register_handler
from handlers.get_user_info import get_user_info_handler
from handlers.put_user_info import put_user_info_handler

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    log.debug("Регистрирую обычного пользователя")
    try:
        data = await request.json()
        registered_user_id: UUID = individual_register_handler(data)
        return {"status": "success", "data": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.post("/register_org")
async def register_org(request: Request):
    log.debug("Регистрирую организацию")
    try:
        data = await request.json()
        registered_org_id: UUID = organization_register_handler(data)
        return {"status": "success", "data": registered_org_id}
    except SpecialException as e: 
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

