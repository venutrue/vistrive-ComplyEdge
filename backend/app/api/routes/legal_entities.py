from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import LegalEntity, Tenant
from app.schemas.legal_entity import LegalEntityCreateRequest, LegalEntityResponse
from app.services.audit import log_event

router = APIRouter(prefix="/legal-entities", tags=["legal-entities"])


@router.post("", response_model=LegalEntityResponse, status_code=status.HTTP_201_CREATED)
def create_legal_entity(payload: LegalEntityCreateRequest, db: Session = Depends(get_db)) -> LegalEntityResponse:
    tenant = db.query(Tenant).filter(Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    entity = LegalEntity(
        tenant_id=payload.tenant_id,
        name=payload.name,
        cin=payload.cin,
        pan=payload.pan,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)

    log_event(db, actor="system", entity_type="legal_entity", entity_id=entity.id, action="created", details=payload.model_dump())
    return LegalEntityResponse.model_validate(entity)


@router.get("/tenant/{tenant_id}", response_model=list[LegalEntityResponse])
def list_legal_entities(tenant_id: str, db: Session = Depends(get_db)) -> list[LegalEntityResponse]:
    entities = db.query(LegalEntity).filter(LegalEntity.tenant_id == tenant_id).all()
    return [LegalEntityResponse.model_validate(e) for e in entities]
