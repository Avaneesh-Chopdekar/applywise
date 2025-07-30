from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from .models import Resume, ResumeUpdate


async def fetch_resumes():
    """List all resumes."""
    resumes = await Resume.find_many().to_list()
    return {"resumes": resumes}


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
    result = await Resume.delete_many({"_id": resume_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )
    return {"message": "Resume deleted successfully"}
