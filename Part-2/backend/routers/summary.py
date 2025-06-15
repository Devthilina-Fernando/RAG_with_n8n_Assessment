from fastapi import APIRouter, HTTPException
from schemas.summary import SummaryRequest, SummaryResponse
from services.summary_service import SummaryService

router = APIRouter()

@router.post("/generate", response_model=SummaryResponse)
async def document_summary(request: SummaryRequest):
    response = SummaryService.generate_summary(request.file_name)
    if not response.success:
        raise HTTPException(status_code=500, detail=response.message)
    return response