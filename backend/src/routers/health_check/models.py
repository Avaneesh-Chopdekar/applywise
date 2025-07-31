from datetime import datetime
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status: str = "ok"
    timestamp: datetime = datetime.utcnow()
