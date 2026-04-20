from app.schemas.common import APIModel


class IncidentCreateRequest(APIModel):
    establishment_id: str
    category: str
    severity: str
    summary: str


class IncidentResponse(APIModel):
    id: str
    establishment_id: str
    category: str
    severity: str
    summary: str
