from datetime import date

from app.schemas.common import APIModel


class ComplianceTaskResponse(APIModel):
    id: str
    establishment_id: str
    obligation_template_id: str
    status: str
    due_date: date
    applicability_reason: str


class GenerateTasksRequest(APIModel):
    establishment_id: str
