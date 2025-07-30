from fastapi import FastAPI


def register_routes(app: FastAPI):
    from .routers.resumes.controller import router as resumes_router

    app.include_router(resumes_router)
