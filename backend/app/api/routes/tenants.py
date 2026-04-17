from uuid import uuid4

from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/tenants", tags=["tenants"])


class TenantCreateRequest(BaseModel):
    legal_name: str
    primary_contact_email: EmailStr


class TenantResponse(BaseModel):
    tenant_id: str
    legal_name: str
    primary_contact_email: EmailStr
    onboarding_status: str


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreateRequest) -> TenantResponse:
    return TenantResponse(
        tenant_id=str(uuid4()),
        legal_name=payload.legal_name,
        primary_contact_email=payload.primary_contact_email,
        onboarding_status="created",
    )
