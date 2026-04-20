from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Tenant
from app.schemas.tenant import TenantCreateRequest, TenantResponse
from app.services.audit import log_event

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreateRequest, db: Session = Depends(get_db)) -> TenantResponse:
    existing = db.query(Tenant).filter(Tenant.primary_contact_email == payload.primary_contact_email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Tenant with primary contact email already exists")

    tenant = Tenant(legal_name=payload.legal_name, primary_contact_email=payload.primary_contact_email)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    log_event(db, actor="system", entity_type="tenant", entity_id=tenant.id, action="created", details=payload.model_dump())
    return TenantResponse.model_validate(tenant)


@router.get("", response_model=list[TenantResponse])
def list_tenants(db: Session = Depends(get_db)) -> list[TenantResponse]:
    tenants = db.query(Tenant).order_by(Tenant.created_at.desc()).all()
    return [TenantResponse.model_validate(t) for t in tenants]
