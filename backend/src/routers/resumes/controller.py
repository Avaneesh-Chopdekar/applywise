from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from .models import Resume, ResumeUpdate

from .service import (
    create_resume,
    delete_resume_by_id,
    fetch_resumes,
    fetch_resume_by_id,
    update_resume,
)

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])


@router.get("/")
async def get_all_resumes():
    resumes = await fetch_resumes()
    return resumes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Resume)
async def post_resume(resume_data: Resume):
    resume = await create_resume(resume_data)
    return resume


@router.get("/{resume_id}", response_model=Resume)
async def get_resume(resume_id: str):
    resume = await fetch_resume_by_id(resume_id)
    return resume


@router.patch(
    "/{resume_id}", response_model=Resume, summary="Partially Update a Resume"
)
async def patch_resume(resume_id: str, update_data: ResumeUpdate):
    updated_resume = await update_resume(resume_id, update_data)
    return updated_resume


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resume(resume_id: str):
    return await delete_resume_by_id(resume_id)
