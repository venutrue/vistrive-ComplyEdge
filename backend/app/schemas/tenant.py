from app.schemas.common import APIModel


class TenantCreateRequest(APIModel):
    legal_name: str
    primary_contact_email: str


class TenantResponse(APIModel):
    id: str
    legal_name: str
    primary_contact_email: str
    onboarding_status: str
