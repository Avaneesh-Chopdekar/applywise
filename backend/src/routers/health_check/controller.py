from fastapi import APIRouter

from .models import HealthCheckResponse

router = APIRouter(prefix="/api/v1/health-check", tags=["Health Check"])


@router.get("/", summary="Health Check", response_model=HealthCheckResponse)
async def health_check():
    """
    Endpoint to check the health of the API.
    Returns a simple status message.
    """
    return HealthCheckResponse(status="ok")
