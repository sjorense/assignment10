from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.base import UserCreate
from app.schemas.user import UserRead


def test_hash_password_returns_verifiable_hash():
    password_hash = User.hash_password("TestPass123")

    assert password_hash != "TestPass123"
    assert User(password_hash=password_hash).verify_password("TestPass123") is True
    assert User(password_hash=password_hash).verify_password("WrongPass123") is False


def test_user_create_validates_email_and_password():
    with pytest.raises(ValidationError):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="not-an-email",
            username="testuser",
            password="TestPass123",
        )

    with pytest.raises(ValidationError):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="weak",
        )


def test_user_read_omits_password_hash():
    schema = UserRead(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="testuser",
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    dumped = schema.model_dump()
    assert "password_hash" not in dumped
    assert "password" not in dumped
