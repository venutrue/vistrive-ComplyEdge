from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Establishment, Incident
from app.schemas.incidents import IncidentCreateRequest, IncidentResponse
from app.services.audit import log_event

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreateRequest, db: Session = Depends(get_db)) -> IncidentResponse:
    establishment = db.query(Establishment).filter(Establishment.id == payload.establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    log_event(db, "system", "incident", incident.id, "created", payload.model_dump())
    return IncidentResponse.model_validate(incident)


@router.get("/establishment/{establishment_id}", response_model=list[IncidentResponse])
def list_incidents(establishment_id: str, db: Session = Depends(get_db)) -> list[IncidentResponse]:
    incidents = db.query(Incident).filter(Incident.establishment_id == establishment_id).all()
    return [IncidentResponse.model_validate(i) for i in incidents]
