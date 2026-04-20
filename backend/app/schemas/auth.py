from app.schemas.common import APIModel


class LoginRequest(APIModel):
    email: str


class LoginResponse(APIModel):
    access_token: str
    token_type: str = "bearer"
    mfa_required: bool


class MfaVerifyRequest(APIModel):
    email: str
    otp_code: str


class MfaVerifyResponse(APIModel):
    verified: bool
