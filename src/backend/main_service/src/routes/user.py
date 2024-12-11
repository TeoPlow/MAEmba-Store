from fastapi import APIRouter, Request
from core.exceptions import SpecialException
from core.auth import login_required
from core.logging import logger_config, log
from handlers.individual_info_changed import individual_info_changed_handler
from handlers.individual_register import individual_register_handler
from handlers.organization_info_changed import organization_info_changed_handler
from handlers.organization_register import organization_register_handler
import logging


logging.config.dictConfig(logger_config)

router = APIRouter()

@login_required
@router.post("/change_info")
async def change_info(request: Request):
    try:
        data = await request.json()
        is_info_changed: bool = individual_info_changed_handler(data)
        return {"status": "success", "data": is_info_changed}
    except SpecialException as e:
        log.info(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@login_required
@router.post("/change_info_org")
async def change_info_org(request: Request):
    try:
        data = await request.json()
        is_info_changed: bool = organization_info_changed_handler(data)
        return {"status": "success", "data": is_info_changed}
    except SpecialException as e: 
        log.info(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/auth/register")
async def register(request: Request):
    try:
        data = await request.json()
        registered_user_id: int = individual_register_handler(data)
        return {"status": "success", "data": registered_user_id}
    except SpecialException as e:
        log.info(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.post("/auth/register_org")
async def register_org(request: Request):
    try:
        data = await request.json()
        registered_user_id: int = organization_register_handler(data)
        return {"status": "success", "data": registered_user_id}
    except SpecialException as e: 
        log.info(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/auth/login")
async def login(request: Request):
    pass

@router.post("/auth/validate-token")
async def validate_token(request: Request):
    pass

@router.get("/{user_id}")
async def get_user_info(request: Request):
    pass

@router.put("/{user_id}")
async def put_user_info(request: Request):
    pass

@router.get("/{org_id}")
async def get_org_info(request: Request):
    pass

@router.put("/{org_id}")
async def put_org_info(request: Request):
    pass


