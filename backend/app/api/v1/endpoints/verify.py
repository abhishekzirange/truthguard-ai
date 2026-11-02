from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.verification import (
    VerificationRequest,
    VerificationRunResponse,
    BatchVerificationRequest,
)
from app.schemas.claim import ClaimResponse
from app.services.verification_service import VerificationService
from app.services.history_service import HistoryService
from app.models import VerificationRun

router = APIRouter()


@router.post("", response_model=VerificationRunResponse, status_code=status.HTTP_201_CREATED)
async def create_verification(
    request: VerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Submits an AI-generated answer for claim extraction, live web search,
    Bifrost AI Gateway assessment, and freshness scoring.
    """
    service = VerificationService(db)
    try:
        run = await service.execute_verification(request)
        return run
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )


@router.get("/{verification_id}", response_model=VerificationRunResponse)
def get_verification_run(
    verification_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves full details of a verification run including extracted claims,
    status assessments, and freshness metrics.
    """
    run = HistoryService.get_run_by_id(db, verification_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification run not found"
        )
    return run


@router.get("/{verification_id}/claims", response_model=List[ClaimResponse])
def get_run_claims(
    verification_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves only the claims and assessments for a specific verification run.
    """
    run = HistoryService.get_run_by_id(db, verification_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification run not found"
        )
    return run.claims


@router.post("/batch", response_model=List[VerificationRunResponse])
async def create_batch_verification(
    batch_req: BatchVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Processes multiple verification requests sequentially with bounded concurrency.
    """
    service = VerificationService(db)
    results = []
    for req in batch_req.items:
        run = await service.execute_verification(req)
        results.append(run)
    return results
