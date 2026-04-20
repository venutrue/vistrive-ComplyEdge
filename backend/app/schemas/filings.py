from app.schemas.common import APIModel


class FilingCreateRequest(APIModel):
    establishment_id: str
    form_name: str
    period_label: str


class FilingResponse(APIModel):
    id: str
    establishment_id: str
    form_name: str
    period_label: str
    status: str


class EvidenceCreateRequest(APIModel):
    filing_id: str
    file_name: str
    storage_path: str


class EvidenceResponse(APIModel):
    id: str
    filing_id: str
    file_name: str
    storage_path: str
