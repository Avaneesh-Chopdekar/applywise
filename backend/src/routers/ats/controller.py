from fastapi import APIRouter


from .service import analyze_resume
from .models import ATSRequest, ATSResponse


router = APIRouter(prefix="/api/v1/ats", tags=["ATS"])


@router.post("/analyze", summary="Analyze Resume", response_model=ATSResponse)
async def post_analyze(request: ATSRequest):
    """
    Analyze a resume based on job description and generate a report and score.
    """

    analysis_result = await analyze_resume(request)
    return analysis_result
