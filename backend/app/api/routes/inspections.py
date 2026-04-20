from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ComplianceTask, Establishment, Filing, Notice
from app.schemas.inspection import InspectionBundleResponse

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.get("/{establishment_id}/bundle", response_model=InspectionBundleResponse)
def inspection_bundle(establishment_id: str, db: Session = Depends(get_db)) -> InspectionBundleResponse:
    establishment = db.query(Establishment).filter(Establishment.id == establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    pending_tasks = db.query(ComplianceTask).filter(ComplianceTask.establishment_id == establishment_id).count()
    filings_count = db.query(Filing).filter(Filing.establishment_id == establishment_id).count()
    notices_count = db.query(Notice).filter(Notice.establishment_id == establishment_id).count()

    return InspectionBundleResponse(
        establishment_id=establishment_id,
        pending_tasks=pending_tasks,
        filings_count=filings_count,
        notices_count=notices_count,
        generated_message="Inspection packet generated with current compliance artifacts.",
    )
