from fastapi import FastAPI


def register_routes(app: FastAPI):
    from .routers.resumes.controller import router as resumes_router
    from .routers.ats.controller import router as ats_router
    from .routers.job_application.controller import router as job_application_router

    app.include_router(resumes_router)
    app.include_router(ats_router)
    app.include_router(job_application_router)
