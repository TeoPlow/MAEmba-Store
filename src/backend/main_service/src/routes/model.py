import requests
from fastapi import APIRouter
from src.core.config import MODEL_API_URL
from src.core.exceptions import SpecialException
from src.core.logging import log

router = APIRouter()


@router.get("/recommendation")
async def recomendation():
    log.debug("Получение списка рекомендаций для пользователя")
    url = MODEL_API_URL + f"/recommendation"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от MODEL API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/predict")
async def predict():
    log.debug("Прогнозирование оптимальной цены товара")
    url = MODEL_API_URL + f"/predict"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от MODEL API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
