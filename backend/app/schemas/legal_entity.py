from typing import Optional

from app.schemas.common import APIModel


class LegalEntityCreateRequest(APIModel):
    tenant_id: str
    name: str
    cin: Optional[str] = None
    pan: Optional[str] = None


class LegalEntityResponse(APIModel):
    id: str
    tenant_id: str
    name: str
    cin: Optional[str] = None
    pan: Optional[str] = None
