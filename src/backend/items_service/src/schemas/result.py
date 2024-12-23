import dataclasses
from pydantic import BaseModel
from typing import Generic, TypeVar

ModelType = TypeVar("ModelType", bound=BaseModel)


@dataclasses.dataclass
class Error:
    reason: str
    code: str

@dataclasses.dataclass
class Result:
    is_success: bool
    error: Error | None
    
    @staticmethod
    def failure(error: Error):
        return Result(is_success=False, error=error)
    
    
    @staticmethod
    def success():
        return Result(is_success=True, error=None)
    

@dataclasses.dataclass
class GenResult(Result, Generic[ModelType]):
    response: ModelType | None
    is_success: bool
    error: Error | None
    
    
    @staticmethod
    def failure(error):
        return GenResult(is_success=False, error=error, response=None)
    
    
    @staticmethod
    def success(value: ModelType):
        return GenResult(is_success=True, error=None, response=value)
