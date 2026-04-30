"""Authenticated encryption helpers for PII fields."""
import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.api.core.config import settings

def _get_key() -> bytes:
    key = settings.ENCRYPTION_KEY.encode("utf-8")
    return key[:32].ljust(32, b"0")


def encrypt_text(plain_text: str) -> str:
    nonce = os.urandom(12)
    ct = AESGCM(_get_key()).encrypt(nonce, plain_text.encode("utf-8"), None)
    return base64.urlsafe_b64encode(nonce + ct).decode("utf-8")


def decrypt_text(encrypted_text: str) -> str | None:
    if not encrypted_text or not isinstance(encrypted_text, (str, bytes)):
        return None
    raw = base64.urlsafe_b64decode(
        encrypted_text.encode("utf-8")
        if isinstance(encrypted_text, str)
        else encrypted_text
    )
    nonce, ct = raw[:12], raw[12:]
    return AESGCM(_get_key()).decrypt(nonce, ct, None).decode("utf-8")


def encrypt_email(plain_email: str) -> str:
    return encrypt_text(plain_email)


def decrypt_email(encrypted_email: str) -> str | None:
    return decrypt_text(encrypted_email)
