from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from beanie import Document, Indexed


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


class ATSAnalysis(Document):
    """
    Model for the analysis of a resume, stored in the database.
    It will embed the ATSCoreOutput.
    """

    llm_analysis: ATSCoreOutput

    job_title: str = Indexed(str, unique=True)
    job_description: str
    resume_id: str = Indexed(str)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "ats_analyses"


class ATSResponse(ATSCoreOutput):
    """
    Model for the HTTP response of the ATS analysis endpoint.
    This will be a subset of ATSAnalysis, containing just the LLM-derived data.
    """

    pass
