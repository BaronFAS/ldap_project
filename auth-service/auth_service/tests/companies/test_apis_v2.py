import json
import pytest

from rest_framework import status

from companies.models import Company


LOCAL_TEST_URL_COMPANIES = "http://127.0.0.1:8000/api/v2/companies/"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_200_OK),
    ],
)
def test_get_list_company(
    client, user, company, company_factory, is_logged_in, expected_status
):
    """An authorized user can receive a list of
    companies that only includes his company."""
    company_factory.create_batch(3)
    user.company = company
    user.save()
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_COMPANIES)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert response.data["results"][0]["id"] == company.id
        assert len(response.data["results"]) == 1


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
    company_factory,
    is_logged_in,
    expected_status
):
    """Super User can get a list of all companies."""
    company_factory.create_batch(3)
    user.is_superuser = True
    user.save()
    if is_logged_in:
        client.force_login(user)
    response = client.get(LOCAL_TEST_URL_COMPANIES)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        all_company = Company.objects.all()
        assert len(response.data['results']) == len(all_company)


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
    is_logged_in,
    expected_status
):
    """The user can get the company by id."""
    if is_logged_in:
        client.force_login(user)
    response = client.get(f"{LOCAL_TEST_URL_COMPANIES}{company.id}/")
    if expected_status == status.HTTP_200_OK:
        company = Company.objects.get(id=response.data["id"])
        assert response.data["name"] == company.name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_201_CREATED),
    ],
)
def test_post_company(client, user, is_logged_in, expected_status):
    """The user can create a company."""
    company_data = {
        "name": "test",
        "short_name": "test",
        "domain_url": "http://test.com",
        "password_reset_uri": "http://test.com/1/",
    }
    if is_logged_in:
        client.force_login(user)
    response = client.post(
        LOCAL_TEST_URL_COMPANIES,
        json.dumps(company_data),
        content_type="application/json",
    )
    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
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
def test_put_company(client, user, company, is_logged_in, expected_status):
    """The user can change the company."""
    company_data_change = {
        "name": "test1",
        "short_name": "t1",
        "domain_url": "http://test1.com",
        "password_reset_uri": "http://test1.com/1/",
    }
    if is_logged_in:
        client.force_login(user)
    response = client.put(
        f"{LOCAL_TEST_URL_COMPANIES}{company.id}/",
        json.dumps(company_data_change),
        content_type="application/json",
    )
    assert response.status_code == expected_status
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
def test_patch_company(client, user, company, is_logged_in, expected_status):
    """The user can change the company."""
    company_data_change = {
        "name": "test1",
    }
    if is_logged_in:
        client.force_login(user)
    response = client.patch(
        f"{LOCAL_TEST_URL_COMPANIES}{company.id}/",
        json.dumps(company_data_change),
        content_type="application/json",
    )
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        company = Company.objects.get(id=response.data["id"])
        assert response.data["name"] == company.name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_logged_in, expected_status",
    [
        (False, status.HTTP_403_FORBIDDEN),
        (True, status.HTTP_204_NO_CONTENT),
    ],
)
def test_delete_company(client, user, company, is_logged_in, expected_status):
    """The user can delete the company."""
    if is_logged_in:
        client.force_login(user)
    response = client.delete(
        f"{LOCAL_TEST_URL_COMPANIES}{company.id}/",
    )
    assert response.status_code == expected_status
    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(company.DoesNotExist):
            Company.objects.get(id=company.id)
