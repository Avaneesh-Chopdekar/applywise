import json

import os
from fastapi import HTTPException, status
from groq import Groq

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

        llm_output = json.loads(llm_raw_content)

        output_dict = dict(
            relevance_score=llm_output["relevance_score"],
            skills=llm_output["skills"],
            total_years_of_experience=llm_output["total_years_of_experience"],
            project_categories=llm_output["project_categories"],
        )

        # ats_analysis = ATSAnalysis(
        #     **output_dict,
        #     job_title=request.job_title,
        #     job_description=request.job_description,
        #     resume_id=request.resume_id,
        # )

        # await ats_analysis.insert()

        return ATSResponse(**output_dict)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM returned invalid JSON: {llm_raw_content}. Error: {str(e)}",
        )
    except Exception as e:
        print(f"Detailed error in analyze_resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}",
        )
