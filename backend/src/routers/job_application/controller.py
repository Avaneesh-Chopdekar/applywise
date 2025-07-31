from datetime import date
from typing import Literal, Optional
from fastapi import APIRouter, Query, Request, status

from ...rate_limiter import limiter
from .models import (
    JobApplication,
    JobApplicationListItem,
    JobApplicationUpdate,
    PaginatedJobApplications,
)
from .service import (
    create_job_application,
    get_job_application_by_id,
    update_job_application,
    delete_job_application_by_id,
    fetch_job_applications,
)

router = APIRouter(prefix="/api/v1/job_applications", tags=["Job Applications"])


@router.get(
    "/",
    response_model=PaginatedJobApplications,
    summary="List all job applications with pagination and filters",
)
@limiter.limit("10/minute;50/hour")
async def list_job_applications(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    user_id: Optional[str] = Query(
        None, description="Filter by specific user ID (required for typical usage)"
    ),
    job_title: Optional[str] = Query(
        None, description="Filter by job title (case-insensitive partial match)"
    ),
    company_name: Optional[str] = Query(
        None, description="Filter by company name (case-insensitive partial match)"
    ),
    status: Optional[str] = Query(None, description="Filter by application status"),
    min_application_date: Optional[date] = Query(
        None, description="Filter by application date (from)"
    ),
    max_application_date: Optional[date] = Query(
        None, description="Filter by application date (to)"
    ),
    has_notes: Optional[bool] = Query(None, description="Filter by presence of notes"),
    has_interviews: Optional[bool] = Query(
        None, description="Filter by presence of interview dates"
    ),
    sort_by: Literal[
        "application_date", "last_updated", "job_title", "company_name"
    ] = Query("application_date", description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query(
        "desc", description="Sort order (asc/desc)"
    ),
):
    """
    Retrieves a paginated list of job applications, with optional filtering and sorting.
    """
    applications = await fetch_job_applications(
        page=page,
        page_size=page_size,
        user_id=user_id,
        job_title=job_title,
        company_name=company_name,
        status=status,
        min_application_date=min_application_date,
        max_application_date=max_application_date,
        has_notes=has_notes,
        has_interviews=has_interviews,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return applications


@router.get(
    "/{app_id}",
    response_model=JobApplication,
    summary="Get a single job application by ID",
)
@limiter.limit("5/minute;20/hour")
async def get_job_application(request: Request, app_id: str):
    """
    Retrieves a single job application by its ID.
    """
    application = await get_job_application_by_id(app_id)
    return application


@router.post(
    "/",
    response_model=JobApplicationListItem,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new job application entry",
)
@limiter.limit("5/minute;20/hour")
async def post_job_application(request: Request, job_application: JobApplication):
    """
    Creates a new job application entry.
    """
    new_application = await create_job_application(job_application)
    return new_application


@router.patch(
    "/{app_id}",
    response_model=JobApplicationListItem,
    summary="Partially update a job application entry",
)
@limiter.limit("5/minute;20/hour")
async def patch_job_application(
    request: Request, app_id: str, update_data: JobApplicationUpdate
):
    """
    Partially updates an existing job application entry.
    """
    updated_appication = await update_job_application(app_id, update_data)
    return updated_appication


@router.delete(
    "/{app_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a job application entry",
)
@limiter.limit("5/minute;20/hour")
async def delete_job_application(request: Request, app_id: str):
    return await delete_job_application_by_id(app_id)
