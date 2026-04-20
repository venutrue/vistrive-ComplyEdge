import base64
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from app.schemas.auth import LoginRequest, LoginResponse, MfaVerifyRequest, MfaVerifyResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _issue_token(email: str) -> str:
    payload = f"{email}|{int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())}"
    return base64.urlsafe_b64encode(payload.encode()).decode()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    return LoginResponse(access_token=_issue_token(payload.email), mfa_required=True)


@router.post("/mfa/verify", response_model=MfaVerifyResponse)
def verify_mfa(payload: MfaVerifyRequest) -> MfaVerifyResponse:
    return MfaVerifyResponse(verified=payload.otp_code == "123456")
