from typing import List, Optional
from datetime import datetime

from beanie import Document
from pydantic import BaseModel, Field, EmailStr


class Contact(BaseModel):
    """Pydantic model for contact information."""

    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class Education(BaseModel):
    """Pydantic model for an education entry."""

    institution: str
    location: Optional[str] = None
    degree: str
    major: Optional[str] = None
    minor: Optional[str] = None
    start_date: Optional[str] = None  # e.g., "Aug. 2018"
    end_date: Optional[str] = None  # e.g., "May 2021"
    description: Optional[List[str]] = Field(default_factory=list)  # Optional notes


class Experience(BaseModel):
    """Pydantic model for an experience entry."""

    title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: List[str] = Field(default_factory=list)  # Array of bullet points


class Project(BaseModel):
    """Pydantic model for a project entry."""

    name: str
    technologies: Optional[str] = None  # "Python, Flask, React, PostgreSQL, Docker"
    date_range: Optional[str] = None  # "June 2020 -- Present"
    link: Optional[str] = None  # Optional: Link to project
    description: List[str] = Field(default_factory=list)  # Array of bullet points


class SkillCategory(BaseModel):
    """Pydantic model for a skill category."""

    category: str  # e.g., "Languages"
    items: str  # "Java, Python, C/C++, SQL (Postgres), JavaScript, HTML/CSS, R"


class Resume(Document):
    """Main Pydantic model for a resume document."""

    user_id: str = Field(unique=True)
    name: str
    contact: Optional[Contact] = None
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: List[SkillCategory] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "resumes"

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        await super().save(*args, **kwargs)


class ResumeUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[Contact] = None
    education: Optional[List[Education]] = None
    experience: Optional[List[Experience]] = None
    projects: Optional[List[Project]] = None
    skills: Optional[List[SkillCategory]] = None
