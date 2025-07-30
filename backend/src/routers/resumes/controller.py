from datetime import datetime
from typing import Literal, Optional
from fastapi import APIRouter, Query, status
from .models import PaginatedResumes, Resume, ResumeUpdate

from .service import (
    create_resume,
    delete_resume_by_id,
    fetch_resumes,
    fetch_resume_by_id,
    update_resume,
)

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])


@router.get("/", response_model=PaginatedResumes, summary="List Resumes")
async def get_all_resumes(
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    # Filtering options
    search_name: Optional[str] = Query(
        None, description="Search by resume name (case-insensitive)"
    ),
    starred: Optional[bool] = Query(
        None, description="Filter by starred status (true/false)"
    ),
    min_created_at: Optional[datetime] = Query(
        None, description="Filter by creation date (from)"
    ),
    max_created_at: Optional[datetime] = Query(
        None, description="Filter by creation date (to)"
    ),
    # Sorting options
    sort_by: Literal["created_at", "updated_at", "name"] = Query(
        "created_at", description="Field to sort by"
    ),
    sort_order: Literal["asc", "desc"] = Query(
        "desc", description="Sort order (asc/desc)"
    ),
):
    resumes = await fetch_resumes(
        search_name=search_name,
        starred=starred,
        min_created_at=min_created_at,
        max_created_at=max_created_at,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
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
