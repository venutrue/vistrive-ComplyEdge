from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Establishment, LegalEntity
from app.schemas.establishment import EstablishmentCreateRequest, EstablishmentResponse
from app.services.audit import log_event

router = APIRouter(prefix="/establishments", tags=["establishments"])


@router.post("", response_model=EstablishmentResponse, status_code=status.HTTP_201_CREATED)
def create_establishment(payload: EstablishmentCreateRequest, db: Session = Depends(get_db)) -> EstablishmentResponse:
    legal_entity = db.query(LegalEntity).filter(LegalEntity.id == payload.legal_entity_id).first()
    if not legal_entity:
        raise HTTPException(status_code=404, detail="Legal entity not found")

    establishment = Establishment(
        legal_entity_id=payload.legal_entity_id,
        name=payload.name,
        state=payload.state,
        employee_count=payload.employee_count,
    )
    db.add(establishment)
    db.commit()
    db.refresh(establishment)

    log_event(
        db,
        actor="system",
        entity_type="establishment",
        entity_id=establishment.id,
        action="created",
        details=payload.model_dump(),
    )
    return EstablishmentResponse.model_validate(establishment)


@router.get("/legal-entity/{legal_entity_id}", response_model=list[EstablishmentResponse])
def list_establishments(legal_entity_id: str, db: Session = Depends(get_db)) -> list[EstablishmentResponse]:
    establishments = db.query(Establishment).filter(Establishment.legal_entity_id == legal_entity_id).all()
    return [EstablishmentResponse.model_validate(e) for e in establishments]
