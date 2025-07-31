from datetime import date, datetime
from typing import List, Optional
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field, HttpUrl
from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFER_RECEIVED = "Offer Received"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"


class JobApplication(Document):
    """
    Pydantic and Beanie model for a job application entry.
    """

    user_id: str = Indexed(str)

    job_title: str
    company_name: str
    company_website: Optional[HttpUrl] = None
    job_url: Optional[HttpUrl] = None
    location: Optional[str] = None

    status: ApplicationStatus = Field(
        default=ApplicationStatus.APPLIED,
        description="Current status of the job application",
    )
    application_date: date = Field(default_factory=date.today)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    interview_dates: List[date] = Field(default_factory=list)
    notes: Optional[str] = None

    associated_resume_id: Optional[PydanticObjectId] = Field(
        default=None, description="ID of the resume used for this application"
    )
    associated_analysis_id: Optional[PydanticObjectId] = Field(
        default=None, description="ID of the ATS analysis for this application"
    )

    class Settings:
        name = "job_applications"

    async def save(self, *args, **kwargs):
        self.last_updated = datetime.utcnow()
        await super().save(*args, **kwargs)
