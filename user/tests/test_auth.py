# users/tests/test_auth.py
import pytest
from rest_framework.test import APIClient
from user.infrastructure.models import CustomUser

@pytest.mark.django_db
def test_register_and_login_flow():
    client = APIClient()

    # Register new admin user
    register_data = {
        "email": "admin@bakery.com",
        "name": "Admin Bakery",
        "password": "supersecret123",
    }
    res = client.post("/api/auth/register/", register_data)
    assert res.status_code == 201

    # Login
    login_data = {"email": "admin@bakery.com", "password": "supersecret123"}
    res = client.post("/api/auth/login/", login_data)
    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data
    assert res.data["user"]["email"] == "admin@bakery.com"
