import pytest

from rest_framework import status

from companies.models import Company


LOCAL_TEST_URL_COMPANIES = "http://127.0.0.1:8000/api/v2/external_services/companies/" # noqa
LOCAL_TEST_URL_USER = "http://127.0.0.1:8000/api/v2/external_services/users/"
LOCAL_TEST_URL_ROLE = "http://127.0.0.1:8000/api/v2/external_services/roles/"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
)
def test_only_get_requests_allowed_by_company(
    client,
    user,
    company,
    role,
    is_logged_in,
    expected_status
):
    """Authorized and non-authorized user receive
    403 for any requests except GET."""
    if is_logged_in:
        client.force_login(user)

    url_ids = {
        LOCAL_TEST_URL_COMPANIES: company.id,
        LOCAL_TEST_URL_USER: user.id,
        LOCAL_TEST_URL_ROLE: role.id,
    }

    for url, id in url_ids.items():
        response = client.post(f"{url}")
        assert response.status_code == expected_status
        response = client.put(f"{url}{id}/")
        assert response.status_code == expected_status
        response = client.patch(f"{url}{id}/")
        assert response.status_code == expected_status
        response = client.delete(f"{url}{id}/")
        assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_list_company(
    client,
    user,
    company,
    services,
    company_factory,
    is_logged_in,
    expected_status,
):
    """An authorized user can receive a list of
    companies that only includes his company."""
    company_factory.create_batch(3)
    user.company = company
    user.save()
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_COMPANIES, headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert response.data[0]["id"] == str(company.id)
        assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_company_list_superuser(
    client,
    user,
    services,
    company_factory,
    is_logged_in,
    expected_status,
):
    """Super User can get a list of all companies."""
    company_factory.create_batch(3)
    user.is_superuser = True
    user.save()
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_COMPANIES, headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        all_company = Company.objects.all()
        assert len(response.data) == len(all_company)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_201_CREATED),
    ],
)
def test_get_company_by_id(
    client,
    user,
    company,
    services,
    is_logged_in,
    expected_status,
):
    """The user can get the company by id."""
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    if is_logged_in:
        client.force_login(user)
    response = client.get(
        f"{LOCAL_TEST_URL_COMPANIES}{company.id}/",
        headers=headers
    )
    if expected_status == status.HTTP_200_OK:
        company = Company.objects.get(id=response.data["id"])
        assert response.data["name"] == company.name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_list_user(
    client, user, services, user_factory, is_logged_in, expected_status,
):
    """An authorized user can receive a list of users."""
    user_factory.create_batch(3)
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_USER, headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_user_by_id(client, user, services, is_logged_in, expected_status,):
    """The user can get the user by id."""
    if is_logged_in:
        client.force_login(user)
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    response = client.get(f"{LOCAL_TEST_URL_USER}{user.id}/", headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert response.data["id"] == str(user.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_list_role(
    client, user, services, role_factory, is_logged_in, expected_status,
):
    """An authorized user can receive a list of roles."""
    role_factory.create_batch(3)
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_ROLE, headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert len(response.data) == 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_role_by_id(
    client, user, services, role, is_logged_in, expected_status,
):
    """The user can get the role by id."""
    if is_logged_in:
        client.force_login(user)
    headers = {
            "JWT-Custom-Header": services.jwt_token
        }
    response = client.get(f"{LOCAL_TEST_URL_ROLE}{role.id}/", headers=headers)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert response.data["id"] == role.id
