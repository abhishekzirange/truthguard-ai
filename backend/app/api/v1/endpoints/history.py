from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.verification import VerificationRunListItem
from app.services.history_service import HistoryService

router = APIRouter()


@router.get("", response_model=List[VerificationRunListItem])
def get_verification_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Returns historical verification runs with summary stats and timestamps.
    """
    return HistoryService.get_runs(db, skip=skip, limit=limit)
