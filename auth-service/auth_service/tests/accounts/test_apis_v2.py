import json
import pytest

from rest_framework import status

from accounts.models import User, Role


LOCAL_TEST_URL_USER = "http://127.0.0.1:8000/api/v2/users/"
LOCAL_TEST_URL_ROLE = "http://127.0.0.1:8000/api/v2/roles/"


@pytest.fixture
def role(role_factory):
    """A fixture that creates a role."""
    return role_factory()


@pytest.fixture
def company(company_factory):
    """A fixture that creates a company."""
    return company_factory()


@pytest.fixture
def user(user_factory, company, role_factory):
    """A fixture that creates a user."""
    user = user_factory(company=company)
    role = role_factory()
    user.role.add(role)
    return user


@pytest.mark.django_db
def test_get_unauthorized_user(client):
    """Check that an unauthorized user cannot obtain the list of users."""
    response = client.get(LOCAL_TEST_URL_USER)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_user_list_superuser(client, user, user_factory):
    """Check that the superuser can get a list of all users."""
    user_factory.create_batch(3)
    user.is_superuser = True
    user.save()
    client.force_login(user)
    response = client.get(LOCAL_TEST_URL_USER)
    assert response.status_code == status.HTTP_200_OK
    users = User.objects.all()
    assert len(response.data["results"]) == len(users)


@pytest.mark.django_db
def test_get_user_list_same_company(
    client, user, company, user_factory, company_factory
):
    """They will check that the user can get a
    list of all users of only his company."""
    user = User.objects.get(email=user.email)
    user.company = company
    user.save()
    client.force_login(user)

    user_factory.create_batch(3, company=company)
    new_company = company_factory()
    user_factory.create_batch(3, company=new_company)

    response = client.get(LOCAL_TEST_URL_USER)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4
    """Let's check that there are 4 users in the company,
    3 saved data and who made the request."""
    expected_company_name = company.name
    for user_data in response.data["results"]:
        assert user_data["company_name"] == expected_company_name
    assert len(User.objects.all()) == 7
    # Check that a total of 7 users have been created


@pytest.mark.django_db
def test_get_user(client, user_factory, company):
    """Checks receipt of user by ID."""
    user = user_factory.build(company=company)
    client.force_login(user)

    test_user = user_factory.build(company=company)
    test_user.save()
    test_user_id = test_user.id

    response = client.get(f"{LOCAL_TEST_URL_USER}{test_user_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == test_user.email


@pytest.mark.django_db
def test_post_user(client, user, company, role_factory):
    """They will check that the user can create a
    user only within his own company."""
    roles = role_factory.create_batch(2)
    role_ids = [role.id for role in roles]
    user_data = {
        "email": "test@test.com",
        "first_name": "Fooo",
        "last_name": "Bar",
        "phone_number": "19997778822",
        "is_active": True,
        "role_ids": role_ids,
        "company_id": str(company.id),
    }

    client.force_login(user)
    response = client.post(
        LOCAL_TEST_URL_USER, json.dumps(user_data),
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_201_CREATED
    for key, value in user_data.items():
        if key == "role_ids" or key == "company_id":
            continue
        assert response.data[key] == value
    assert response.data["role"] == [roles[0].name, roles[1].name]
    assert response.data["company_name"] == company.name
    assert User.objects.get(email="test@test.com").email == "test@test.com"


@pytest.mark.django_db
def test_post_user_with_forbidden_characters_and_phone_number(
    client, user, company, role_factory
):
    """They will check that when creating a user you cannot use
    forbidden characters and the correct phone number must be used."""
    roles = role_factory.create_batch(2)
    role_ids = [role.id for role in roles]
    forbidden_characters = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[",
        "]", "{", "}", "|", ";", ":", "<", ">", ",", ".",
        "?", "/", " ", "?", "#",
    ]
    for character in forbidden_characters:
        user_data = {
            "email": f"test{character}@test.com",
            "first_name": f"{character}Fooo",
            "last_name": f"{character}Bar",
            "phone_number": f"{character}+19997778822",
            "is_active": True,
            "role_ids": role_ids,
            "company_id": str(company.id),
        }

        client.force_login(user)
        response = client.post(
            LOCAL_TEST_URL_USER,
            json.dumps(user_data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_put_user(client, user_factory, company_factory, role_factory):
    """Check that when using the PUT method the user is updated correctly."""
    company = company_factory.create()

    user = user_factory.build(company=company)
    client.force_login(user)

    test_user = user_factory.build(company=company)
    test_user.save()
    test_user_id = test_user.id

    roles = role_factory.create_batch(2)
    role_ids = [role.id for role in roles]

    updated_test_user_data = {
        "email": "updated@test.com",
        "first_name": "Updated",
        "last_name": "User",
        "phone_number": "1234567890",
        "is_active": False,
        "role_ids": role_ids,
        "company_id": str(company.id),
    }

    response = client.put(
        f"{LOCAL_TEST_URL_USER}{test_user_id}/",
        json.dumps(updated_test_user_data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(id=test_user_id)
    assert user.email == "updated@test.com"
    assert user.first_name == "Updated"
    assert user.last_name == "User"
    assert user.phone_number == "1234567890"
    assert user.is_active is False


@pytest.mark.django_db
def test_patch_user(client, user_factory, company, role_factory):
    """Check that when using the PATC method the user is updated correctly."""
    user = user_factory.build(company=company)
    client.force_login(user)

    test_user = user_factory.build(company=company)
    test_user.save()
    test_user_id = test_user.id

    patched_user_data = {
        "email": "patched@test.com",
        "is_active": False,
    }
    response = client.patch(
        f"{LOCAL_TEST_URL_USER}{test_user_id}/",
        json.dumps(patched_user_data),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(id=test_user_id)
    assert user.email == "patched@test.com"
    assert user.is_active is False


@pytest.mark.django_db
def test_delete_user(client, user_factory, company):
    """Checks user deletion by ID."""
    user = user_factory.build(company=company)
    client.force_login(user)

    test_user = user_factory.build(company=company)
    test_user.save()
    test_user_id = test_user.id

    response = client.delete(f"{LOCAL_TEST_URL_USER}{test_user_id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=test_user_id)


@pytest.mark.django_db
def test_get_role_user(client, user, role_factory):
    """An unauthorized user cannot get a list of all roles
    and one role by id."""
    roles = role_factory.create_batch(2)
    response = client.get(LOCAL_TEST_URL_ROLE)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    client.force_login(user)
    response = client.get(LOCAL_TEST_URL_ROLE)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 3

    for role in roles:
        response = client.get(f"{LOCAL_TEST_URL_ROLE}{role.id}/")
        assert response.data["id"] == role.id
        assert response.data["name"] == role.name


@pytest.mark.django_db
def test_post_put_patch_delete_roles(client, user):
    """Validates user creation and modification of roles."""
    role_data = {
        "name": "test_role"
    }
    response = client.post(
        LOCAL_TEST_URL_ROLE,
        json.dumps(role_data),
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client.force_login(user)
    response = client.post(
        LOCAL_TEST_URL_ROLE,
        json.dumps(role_data),
        content_type="application/json"
    )
    role = Role.objects.get(id=response.data["id"])
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == role.name

    role_data_change = {
        "name": "new_test_role"
    }
    response = client.put(
        f"{LOCAL_TEST_URL_ROLE}{role.id}/",
        json.dumps(role_data_change),
        content_type="application/json"
    )
    role = Role.objects.get(id=response.data["id"])
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == role.name

    response = client.patch(
        f"{LOCAL_TEST_URL_ROLE}{role.id}/",
        json.dumps(role_data),
        content_type="application/json"
    )
    role = Role.objects.get(id=response.data["id"])
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == role.name

    response = client.delete(
        f"{LOCAL_TEST_URL_ROLE}{role.id}/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Role.DoesNotExist):
        Role.objects.get(id=role.id)
