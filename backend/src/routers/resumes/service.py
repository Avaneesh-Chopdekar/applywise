from datetime import datetime
from beanie import SortDirection
from fastapi import HTTPException, status
from .models import PaginatedResumes, Resume, ResumeListItem, ResumeUpdate


async def fetch_resumes(
    search_name: str = None,
    starred: bool = None,
    min_created_at: datetime = None,
    max_created_at: datetime = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
):
    """
    Retrieves a paginated list of all resumes, with optional filtering and sorting.
    """
    query = {}

    if search_name:
        query["name"] = {"$regex": search_name, "$options": "i"}
    if starred is not None:
        query["starred"] = starred
    if min_created_at:
        query["created_at"] = {"$gte": min_created_at}
    if max_created_at:
        if "created_at" in query:
            query["created_at"]["$lte"] = max_created_at
        else:
            query["created_at"] = {"$lte": max_created_at}

    sort_direction = (
        SortDirection.ASCENDING if sort_order == "asc" else SortDirection.DESCENDING
    )
    sort_field = (sort_by, sort_direction)

    total_resumes = await Resume.find(query).count()

    resumes_cursor = Resume.find(query).sort(sort_field)
    resumes = (
        await resumes_cursor.skip((page - 1) * page_size).limit(page_size).to_list()
    )

    items = [
        ResumeListItem.model_validate(resume.model_dump(by_alias=True))
        for resume in resumes
    ]

    return PaginatedResumes(
        total=total_resumes,
        page=page,
        page_size=page_size,
        items=items,
    )


async def create_resume(resume_data: Resume):
    """Create a new resume."""
    existing_resume = await Resume.find_one({"user_id": resume_data.user_id})
    if existing_resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume for this user already exists.",
        )
    await resume_data.insert()
    return resume_data


async def fetch_resume_by_id(resume_id: str):
    """Fetch a resume by its ID."""
    resume = await Resume.find_one({"_id": resume_id})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )
    return resume


async def update_resume(resume_id: str, update_data: ResumeUpdate):
    """Partially update an existing resume."""
    resume = await Resume.find_one({"_id": resume_id})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()

    await resume.update({"$set": update_dict})

    updated_resume = await Resume.find_one({"_id": resume_id})
    if not updated_resume:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve updated resume",
        )

    return updated_resume


async def delete_resume_by_id(resume_id: str):
    """Delete a resume by its ID."""
    result = await Resume.delete({"_id": resume_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )
    return {"message": "Resume deleted successfully"}
