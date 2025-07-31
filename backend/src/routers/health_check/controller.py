from fastapi import APIRouter, Request

from ...rate_limiter import limiter
from .models import HealthCheckResponse

router = APIRouter(prefix="/api/v1/health-check", tags=["Health Check"])


@router.get("/", summary="Health Check", response_model=HealthCheckResponse)
@limiter.limit("100/minute")
async def health_check(request: Request):
    """
    Endpoint to check the health of the API.
    Returns a simple status message.
    """
    return HealthCheckResponse(status="ok")
