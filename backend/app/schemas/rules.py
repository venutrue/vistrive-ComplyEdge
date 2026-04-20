from datetime import date

from app.schemas.common import APIModel


class RegulationCreateRequest(APIModel):
    code_name: str


class RegulationResponse(APIModel):
    id: str
    code_name: str
    active: bool


class RuleCreateRequest(APIModel):
    regulation_id: str
    name: str
    state: str = "ALL"
    min_employee_threshold: int = 1
    effective_from: date
    source_reference: str


class RuleResponse(APIModel):
    id: str
    regulation_id: str
    name: str
    state: str
    min_employee_threshold: int
    effective_from: date
    source_reference: str


class ObligationTemplateCreateRequest(APIModel):
    rule_id: str
    name: str
    cadence: str
    sla_days: int = 7


class ObligationTemplateResponse(APIModel):
    id: str
    rule_id: str
    name: str
    cadence: str
    sla_days: int
