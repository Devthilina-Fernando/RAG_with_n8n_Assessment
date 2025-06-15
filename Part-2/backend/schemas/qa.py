from pydantic import BaseModel
from schemas.base import ResponseModel

class QuestionRequest(BaseModel):
    question: str

class QAResponse(ResponseModel):
    data: dict = {
        "answer": None,
        "sources": None
    }