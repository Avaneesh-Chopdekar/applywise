from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import init_db
from .logging import configure_logging, LogLevels
from .register_routes import register_routes


configure_logging(LogLevels.info)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="ApplyWise API",
    description="Create and manage job applications and resumes with ApplyWise and get insights from ATS analysis.",
    version="1.0.0",
)


register_routes(app)
