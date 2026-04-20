from app.schemas.common import APIModel


class DashboardSummary(APIModel):
    total_tenants: int
    total_establishments: int
    total_tasks: int
    overdue_tasks: int
    open_notices: int
    draft_filings: int
