from app.schemas.common import APIModel


class CopilotQueryRequest(APIModel):
    tenant_id: str
    question: str


class CopilotResponse(APIModel):
    answer: str
    confidence: float
    citations: list[str]
    requires_human_review: bool
