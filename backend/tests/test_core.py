from app.services.ingestion import safe_public_url
from app.core.security import hash_password, verify_password


def test_safe_public_url():
    assert safe_public_url("https://www.rbi.org.in/report")
    assert not safe_public_url("http://localhost/private")
    assert not safe_public_url("file:///etc/passwd")


def test_password_roundtrip():
    encoded = hash_password("ValidPass123!")
    assert verify_password("ValidPass123!", encoded)
    assert not verify_password("wrong", encoded)

