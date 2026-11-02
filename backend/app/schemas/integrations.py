from typing import Optional
from pydantic import BaseModel


class IntegrationStatus(BaseModel):
    configured: bool
    reachable: bool
    latency_ms: Optional[int] = None
    message: str
    details: Optional[dict] = None


class IntegrationsReport(BaseModel):
    tavily: IntegrationStatus
    bifrost: IntegrationStatus
    database: IntegrationStatus

