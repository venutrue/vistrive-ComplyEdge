from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Establishment, EvidenceDocument, Filing
from app.schemas.filings import EvidenceCreateRequest, EvidenceResponse, FilingCreateRequest, FilingResponse
from app.services.audit import log_event

router = APIRouter(prefix="/filings", tags=["filings-evidence"])


@router.post("", response_model=FilingResponse, status_code=status.HTTP_201_CREATED)
def create_filing(payload: FilingCreateRequest, db: Session = Depends(get_db)) -> FilingResponse:
    establishment = db.query(Establishment).filter(Establishment.id == payload.establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    filing = Filing(**payload.model_dump())
    db.add(filing)
    db.commit()
    db.refresh(filing)
    log_event(db, "system", "filing", filing.id, "created", payload.model_dump())
    return FilingResponse.model_validate(filing)


@router.post("/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def attach_evidence(payload: EvidenceCreateRequest, db: Session = Depends(get_db)) -> EvidenceResponse:
    filing = db.query(Filing).filter(Filing.id == payload.filing_id).first()
    if not filing:
        raise HTTPException(status_code=404, detail="Filing not found")

    evidence = EvidenceDocument(**payload.model_dump())
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    log_event(db, "system", "evidence_document", evidence.id, "attached", payload.model_dump())
    return EvidenceResponse.model_validate(evidence)
