from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.evidence import EvidenceResponse
from app.models import Claim

router = APIRouter()


@router.get("/{claim_id}/evidence", response_model=List[EvidenceResponse])
def get_claim_evidence(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves normalized evidence retrieved for a specific claim.
    """
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    return claim.evidence_items

