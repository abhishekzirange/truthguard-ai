from fastapi import APIRouter
from app.api.v1.endpoints import (
    verify,
    claims,
    history,
    metrics,
    health,
    integrations,
)

api_router = APIRouter()

api_router.include_router(verify.router, prefix="/verify", tags=["Verification"])
api_router.include_router(claims.router, prefix="/claims", tags=["Claims & Evidence"])
api_router.include_router(history.router, prefix="/history", tags=["History"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Metrics & Analytics"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
