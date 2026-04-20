from app.schemas.common import APIModel


class NotificationCreateRequest(APIModel):
    tenant_id: str
    channel: str
    subject: str
    body: str


class NotificationResponse(APIModel):
    id: str
    tenant_id: str
    channel: str
    subject: str
    body: str
    status: str
