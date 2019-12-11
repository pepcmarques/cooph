from coop.accounts.models import User
from django_dynamic_fixture import G
import pytest


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user for a test"""
    email = 'test_user@this.is.a.test'
    password = '1t_c0uld_b3_ch4nged'
    user = G(User, email=email)
    user.set_password(password)
    user.save()
    client.login(email=email, password=password)
    return user
