from pydantic import BaseModel
from schemas.base import ResponseModel

class SummaryRequest(BaseModel):
    file_name: str

class SummaryResponse(ResponseModel):
    data: dict = {
        "summary": None
    }