from fastapi import APIRouter, HTTPException
from schemas.qa import QuestionRequest, QAResponse
from services.qa_service import QAService

router = APIRouter()
qa_service = QAService()

@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    response = qa_service.ask_question(request.question)
    if not response.success:
        raise HTTPException(status_code=500, detail=response.message)
    return response