from fastapi.responses import JSONResponse
from src.core.logging import log

# Класс для ловли исключений
class SpecialException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


async def special_exception_handler(request, exc: SpecialException):
    """
    Обработчик для SpecialException.
    Возвращает JSON с кастомным сообщением.
    """
    log.warning(exc.message)
    return JSONResponse(
        content={"status": "warning", "message": exc.message},
    )