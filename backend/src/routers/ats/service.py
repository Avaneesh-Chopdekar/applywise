from datetime import datetime
import json

import os
from fastapi import HTTPException, status
from groq import Groq
from pydantic import ValidationError

from .models import ATSCoreOutput, ATSRequest, ATSAnalysis, ATSResponse
from ..resumes.models import Resume


async def analyze_resume(request: ATSRequest) -> ATSAnalysis:
    """
    Analyze a resume based on job description and generate a report and score.
    """

    resume = await Resume.get(request.resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    resume_data_for_llm = resume.model_dump(
        mode="json", exclude_unset=True, by_alias=False
    )

    prompt = f"""
    You are an AI assistant that analyzes resumes for a software engineering job application.
    Given a resume and a job description, extract the following details:

    1. Identify all skills mentioned in the resume.
    2. Calculate the total years of experience.
    3. Categorize the projects based on the domain (e.g., "Web Development", "Data Science", "Mobile", "Backend", "Frontend", "Game Development").
    4. Rank the resume relevance to the job description on a scale of 0 to 100.

    Resume Data:
    {json.dumps(resume_data_for_llm, indent=2)}

    Job Description:
    {request.job_description}

    Provide the output in valid JSON format with this structure:
    {{
        "relevance_score": "<percentage: int>",
        "skills": ["skill1", "skill2", ......],
        "total_years_of_experience": "<number of years: int>",
        "project_categories": ["category1", "category2", ....]
    }}
    """

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        llm_raw_content = response.choices[0].message.content

        llm_output_dict = json.loads(llm_raw_content)

        core_analysis_data = ATSCoreOutput.model_validate(llm_output_dict)

        ats_analysis_to_store = ATSAnalysis(
            llm_analysis=core_analysis_data,
            job_title=request.job_title,
            job_description=request.job_description,
            resume_id=request.resume_id,
        )

        await ats_analysis_to_store.insert()

        return ATSResponse(**core_analysis_data.model_dump())

    except ValidationError as e:
        print(f"Pydantic Validation Error: {e.errors()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Data validation failed: {e.errors()}",
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM returned invalid JSON: {llm_raw_content}. Error: {str(e)}",
        )
    except Exception as e:
        print(f"General error in analyze_resume: {e.__class__.__name__}: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during resume analysis: {str(e)}",
        )


async def delete_analysis_by_id(analysis_id: str) -> None:
    """
    Delete an ATS analysis by its ID.
    """
    analysis = await ATSAnalysis.get(analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ATS Analysis not found"
        )

    await analysis.delete()
    return {"detail": "ATS Analysis deleted successfully"}


async def list_ats_analyses(
    resume_id: str = None,
    job_title: str = None,
    skip: int = 0,
    limit: int = 10,
) -> list[ATSAnalysis]:
    """
    List all ATS analyses, optionally filtered by resume ID and/or job title, with pagination.
    """
    query = {}

    if resume_id:
        query["resume_id"] = resume_id
    if job_title:
        query["job_title"] = job_title

    if query:
        analyses = await ATSAnalysis.find(query).skip(skip).limit(limit).to_list()
    else:
        analyses = await ATSAnalysis.find_all().skip(skip).limit(limit).to_list()

    return analyses


async def update_title_and_description(
    analysis_id: str, job_title: str, job_description: str
) -> ATSAnalysis:
    """
    Update the job title and description of an existing ATS analysis.
    """
    analysis = await ATSAnalysis.get(analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ATS Analysis not found"
        )

    analysis.job_title = job_title
    analysis.job_description = job_description

    await analysis.save()

    return analysis
