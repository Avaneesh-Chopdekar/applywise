from datetime import datetime
from beanie import PydanticObjectId, SortDirection
from fastapi import HTTPException, status

from .models import (
    JobApplication,
    JobApplicationListItem,
    JobApplicationUpdate,
    PaginatedJobApplications,
)
from .exceptions import (
    InvalidIDFormatError,
    JobApplicationAlreadyExistsError,
    JobApplicationNotFoundError,
)


async def fetch_job_applications(
    page: int = 1,
    page_size: int = 10,
    user_id: str = None,
    job_title: str = None,
    company_name: str = None,
    status: str = None,
    min_application_date: datetime = None,
    max_application_date: datetime = None,
    has_notes: bool = None,
    has_interviews: bool = None,
    sort_by: str = "application_date",
    sort_order: str = "desc",
) -> PaginatedJobApplications:
    """
    Fetches a paginated list of job applications with optional filters.
    """
    query = {}

    if user_id:
        query["user_id"] = user_id

    if job_title:
        query["job_title"] = {"$regex": job_title, "$options": "i"}
    if company_name:
        query["company_name"] = {"$regex": company_name, "$options": "i"}
    if status:
        query["status"] = status

    if min_application_date:
        query["application_date"] = {"$gte": min_application_date}
    if max_application_date:
        if "application_date" in query:
            query["application_date"]["$lte"] = max_application_date
        else:
            query["application_date"] = {"$lte": max_application_date}

    if has_notes is not None:
        if has_notes:
            query["notes"] = {"$ne": None, "$ne": ""}
        else:
            query["$or"] = [{"notes": None}, {"notes": ""}]

    if has_interviews is not None:
        if has_interviews:
            query["interview_dates"] = {"$ne": [], "$ne": None}
        else:
            query["$or"] = [
                {"interview_dates": []},
                {"interview_dates": None},
            ]

    sort_direction = (
        SortDirection.ASCENDING if sort_order == "asc" else SortDirection.DESCENDING
    )
    sort_field = (sort_by, sort_direction)

    total_applications = await JobApplication.find(query).count()

    applications_cursor = JobApplication.find(query).sort(sort_field)
    applications = (
        await applications_cursor.skip((page - 1) * page_size)
        .limit(page_size)
        .to_list()
    )

    items = [
        JobApplicationListItem.model_validate(app.model_dump(by_alias=True))
        for app in applications
    ]

    return PaginatedJobApplications(
        total=total_applications,
        page=page,
        page_size=page_size,
        items=items,
    )


async def get_job_application_by_id(app_id: str) -> JobApplication:
    """
    Retrieves a single job application by its ID.
    """
    try:
        app_obj_id = PydanticObjectId(app_id)
    except Exception:
        raise InvalidIDFormatError(id=app_id)

    job_app = await JobApplication.get(app_obj_id)
    if not job_app:
        raise JobApplicationNotFoundError(id=app_id)

    return job_app


async def create_job_application(
    job_application: JobApplication,
) -> JobApplicationListItem:
    """Creates a new job application entry."""
    if hasattr(job_application, "id") and job_application.id is not None:
        existing_application = await JobApplication.get(job_application.id)
        if existing_application:
            raise JobApplicationAlreadyExistsError(id=job_application.id)
    await job_application.insert()
    return job_application


async def update_job_application(
    app_id: str, update_data: JobApplicationUpdate
) -> JobApplicationListItem:
    """
    Partially updates an existing job application entry.
    """

    try:
        app_obj_id = PydanticObjectId(app_id)
    except Exception:
        raise InvalidIDFormatError(id=app_id)

    job_app = await JobApplication.get(app_obj_id)
    if not job_app:
        raise JobApplicationNotFoundError(id=app_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    if (
        "associated_resume_id" in update_dict
        and update_dict["associated_resume_id"] is not None
    ):
        update_dict["associated_resume_id"] = PydanticObjectId(
            update_dict["associated_resume_id"]
        )
    if (
        "associated_analysis_id" in update_dict
        and update_dict["associated_analysis_id"] is not None
    ):
        update_dict["associated_analysis_id"] = PydanticObjectId(
            update_dict["associated_analysis_id"]
        )

    update_dict["last_updated"] = datetime.utcnow()

    await job_app.set(update_dict)

    return JobApplicationListItem.model_validate(job_app.model_dump(by_alias=True))


async def delete_job_application_by_id(app_id: str) -> dict:
    """
    Deletes a job application entry by its ID.
    """
    try:
        app_obj_id = PydanticObjectId(app_id)
    except Exception:
        raise InvalidIDFormatError(id=app_id)

    job_app = await JobApplication.get(app_obj_id)
    if not job_app:
        raise JobApplicationNotFoundError(id=app_id)

    await job_app.delete()
    return {"detail": "Job application deleted successfully"}
