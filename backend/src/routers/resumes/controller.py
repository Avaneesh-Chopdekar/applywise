from fastapi import APIRouter


router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])


@router.get("/")
async def list_resumes():
    return {"message": "List of resumes"}


@router.post("/")
async def create_resume():
    return {"message": "Resume created"}


@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    return {"message": f"Details of resume {resume_id}"}


@router.put("/{resume_id}")
async def update_resume(resume_id: str):
    return {"message": f"Resume {resume_id} updated"}


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    return {"message": f"Resume {resume_id} deleted"}
