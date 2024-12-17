from functools import wraps
from uuid import UUID
from fastapi import Request

from src.core.exceptions import SpecialException
from src.core.logging import log


