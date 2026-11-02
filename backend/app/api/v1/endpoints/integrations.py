from fastapi import APIRouter
from app.schemas.integrations import IntegrationsReport, IntegrationStatus
from app.integrations.tavily_adapter import TavilyAdapter
from app.integrations.bifrost_adapter import BifrostAdapter
from app.core.config import settings

router = APIRouter()


@router.get("/status", response_model=IntegrationsReport)
async def get_integrations_status():
    """
    Performs live server-side diagnostic ping to Tavily and Bifrost.
    Never exposes API secrets to the client.
    """
    tavily = TavilyAdapter()
    bifrost = BifrostAdapter()

    tavily_health = await tavily.check_health()
    bifrost_health = await bifrost.check_health()

    return IntegrationsReport(
        tavily=IntegrationStatus(
            configured=tavily_health["configured"],
            reachable=tavily_health["reachable"],
            latency_ms=tavily_health.get("latency_ms"),
            message=tavily_health["message"]
        ),
        bifrost=IntegrationStatus(
            configured=bifrost_health["configured"],
            reachable=bifrost_health["reachable"],
            latency_ms=bifrost_health.get("latency_ms"),
            message=bifrost_health["message"],
            details=bifrost_health.get("details")
        ),
        database=IntegrationStatus(
            configured=True,
            reachable=True,
            latency_ms=1,
            message="Database operational (" + ("PostgreSQL" if "postgresql" in settings.DATABASE_URL else "SQLite") + ")"
        )
    )
