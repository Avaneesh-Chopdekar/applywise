from typing import List
from fastapi import APIRouter, Request

from ...rate_limiter import limiter
from .service import (
    analyze_resume,
    delete_analysis_by_id,
    list_ats_analyses,
    update_title_and_description,
)
from .models import ATSAnalysis, ATSRequest, ATSResponse


router = APIRouter(prefix="/api/v1/ats", tags=["ATS"])


@router.post("/analyze", summary="Analyze Resume", response_model=ATSResponse)
@limiter.limit("1/10seconds;5/minute;20/hour")
async def post_analyze(request: Request, data: ATSRequest):
    """
    Analyze a resume based on job description and generate a report and score.
    """

    analysis_result = await analyze_resume(data)
    return analysis_result


@router.get(
    "/history", summary="Get ATS Analysis History", response_model=List[ATSAnalysis]
)
@limiter.limit("10/minute;50/hour")
async def get_analysis_history(
    request: Request,
    resume_id: str = None,
    job_title: str = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Get the history of ATS analyses, optionally filtered by resume ID and/or job title.
    """
    analyses = await list_ats_analyses(resume_id, job_title, skip, limit)
    return analyses


@router.put(
    "/history/{analysis_id}",
    summary="Update Job Title and Description of ATS Analysis",
    response_model=ATSAnalysis,
)
@limiter.limit("5/minute;20/hour")
async def update_analysis(
    request: Request, analysis_id: str, job_title: str, job_description: str
):
    """
    Update the job title and description of an existing ATS analysis.
    """
    analysis = await update_title_and_description(
        analysis_id, job_title, job_description
    )
    return analysis


@router.delete("/history/{analysis_id}", summary="Delete ATS Analysis")
@limiter.limit("5/minute;20/hour")
async def delete_analysis(request: Request, analysis_id: str):
    """
    Delete an ATS analysis by its ID.
    """
    return await delete_analysis_by_id(analysis_id)
