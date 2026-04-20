from app.schemas.common import APIModel


class InspectionBundleResponse(APIModel):
    establishment_id: str
    pending_tasks: int
    filings_count: int
    notices_count: int
    generated_message: str
