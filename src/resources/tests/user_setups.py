import pytest

from src.domains.users.entities import UserEntity, UserInputs, UserRole


@pytest.fixture
def user_inputs() -> UserInputs:
    return UserInputs(
        email="john@doe.com",
        username="jonhndoe",
        password="password123",
        first_name="John",
        last_name="Doe",
    )


@pytest.fixture
def user_common() -> UserEntity:
    return UserEntity(
        email="user@common.com",
        username="user_common",
        first_name="User",
        last_name="Common",
        role=UserRole.USER,
    )


@pytest.fixture
def user_admin() -> UserEntity:
    return UserEntity(
        email="user@admin.com",
        username="user_admin",
        first_name="User",
        last_name="Admin",
        role=UserRole.ADMIN,
    )
