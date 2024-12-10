import pytest
from pytest_factoryboy import register
from tests.auth import authenticated_user
from tests.factories import (
    CompanyFactory,
    UserFactory,
    RoleFactory,
    PermissionFactory,
    ServicesFactory
)


register(CompanyFactory)
register(UserFactory)
register(RoleFactory)
register(PermissionFactory)
register(ServicesFactory)


@pytest.fixture()
def services(services_factory):
    return services_factory()


@pytest.fixture()
def role(role_factory):
    return role_factory()


@pytest.fixture()
def company(company_factory):
    return company_factory()


@pytest.fixture()
def expired_user_token():
    return (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTA2NTYxLCJpYXQiOjE2NTQx" # noqa
        "MDYyNjEsImp0aSI6ImNhZGRlZGY2MjcyZjQ2NTFiNTNjODdlZjY4NTViZTUwIiwidXNlcl9pZCI6ImMxM2RiMGI4LWE5ODMtNGI1Yy1hN" # noqa
        "WVkLWNhMTZmZjM5OTAxZSJ9.gqZFrfUk8T7Y03IX-FjzhMdN51Znfame4NQTMH34tGQ"
    )


@pytest.fixture
def auth_user(user_factory):
    with authenticated_user(user_factory()) as u:
        yield u
