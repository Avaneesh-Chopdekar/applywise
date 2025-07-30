from typing import List, Optional
from pydantic import BaseModel, Field
from beanie import Document


class ATSRequest(BaseModel):
    """
    Model for the request to analyze a resume.
    """

    resume_id: str
    job_title: str
    job_description: str


class ATSCoreOutput(BaseModel):
    """
    Core output structure from the LLM.
    """

    relevance_score: int
    skills: List[str]
    total_years_of_experience: int
    project_categories: List[str]


class ATSAnalysis(Document, ATSCoreOutput):
    """
    Model for the analysis of a resume, stored in the database.
    Combines LLM output with job context.
    """

    job_title: str
    job_description: str
    resume_id: str = Field(index=True)

    class Settings:
        name = "ats_analyses"


class ATSResponse(ATSCoreOutput):
    """
    Model for the HTTP response of the ATS analysis endpoint.
    This will be a subset of ATSAnalysis, containing just the LLM-derived data.
    """

    pass
