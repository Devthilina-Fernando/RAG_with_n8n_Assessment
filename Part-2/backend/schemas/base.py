from pydantic import BaseModel

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: dict = None

class ErrorResponse(ResponseModel):
    error_code: str = None
    details: dict = None