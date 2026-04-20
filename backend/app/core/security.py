import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unb64(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def create_access_token(subject: str, tenant_id: str, role: str, minutes: int = 60) -> str:
    settings = get_settings()
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "role": role,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=minutes)).timestamp()),
    }
    payload_raw = json.dumps(payload, separators=(",", ":")).encode()
    payload_part = _b64(payload_raw)
    sig = hmac.new(settings.auth_secret_key.encode(), payload_part.encode(), hashlib.sha256).digest()
    return f"{payload_part}.{_b64(sig)}"


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        payload_part, signature_part = token.split(".", 1)
        expected_sig = hmac.new(settings.auth_secret_key.encode(), payload_part.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64(expected_sig), signature_part):
            raise ValueError("Invalid signature")

        payload = json.loads(_unb64(payload_part).decode())
        if payload.get("exp", 0) < int(datetime.now(timezone.utc).timestamp()):
            raise ValueError("Token expired")
        return payload
    except Exception as exc:
        raise ValueError("Invalid token") from exc
