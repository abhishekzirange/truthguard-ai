from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.metrics import MetricsResponse
from app.services.metrics_service import MetricsService

router = APIRouter()


@router.get("", response_model=MetricsResponse)
def get_metrics(db: Session = Depends(get_db)):
    """
    Returns aggregated metrics, claim category breakdown, and cost estimation.
    """
    return MetricsService.get_dashboard_metrics(db)
