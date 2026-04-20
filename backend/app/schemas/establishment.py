from app.schemas.common import APIModel


class EstablishmentCreateRequest(APIModel):
    legal_entity_id: str
    name: str
    state: str
    employee_count: int


class EstablishmentResponse(APIModel):
    id: str
    legal_entity_id: str
    name: str
    state: str
    employee_count: int
