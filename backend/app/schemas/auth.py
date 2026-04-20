from typing import Optional

from app.schemas.common import APIModel


class LoginRequest(APIModel):
    email: str
    tenant_id: Optional[str] = None
    role: str = "Compliance Admin"
    remember_device: bool = False


class LoginResponse(APIModel):
    access_token: str
    token_type: str = "bearer"
    mfa_required: bool


class MfaVerifyRequest(APIModel):
    email: str
    otp_code: str


class MfaVerifyResponse(APIModel):
    verified: bool
