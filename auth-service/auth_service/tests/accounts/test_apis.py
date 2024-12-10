# import datetime
# import json

import pytest
# from accounts.models import Statuses
from django_scopes import scopes_disabled
from rest_framework import status
from rest_framework.reverse import reverse
from tests.auth import authenticated_user


@pytest.fixture
def auth_user(user_factory):
    return user_factory()


@pytest.fixture
def role(role_factory):
    return role_factory()


@pytest.fixture
def perm1(permission_factory):
    return permission_factory(name="Can Foo", codename="can_foo")


@pytest.fixture
def perm2(permission_factory):
    return permission_factory(name="Can Bar", codename="can_bar")


# @pytest.mark.django_db
# def test_get_user_permissions_with_no_permissions(client, auth_user):
#     """The test checks that the 'user_has_permissions' endpoint is accessible
#     and that an unauthorized user does not have access rights."""
#     with scopes_disabled():
#         with authenticated_user(auth_user):
#             response = client.get(reverse("user_has_permissions"))
#             assert response.status_code == status.HTTP_200_OK

#         assert response.json() == {"permissions": {}}


# # @pytest.mark.django_db
# # def test_get_user_permissions_with_user_permissions(client, auth_user, perm1):
# #     auth_user.user_permissions.add(perm1)
# #     with scopes_disabled():
# #         with authenticated_user(auth_user):
# #             response = client.get(reverse("user_has_permissions"))
# #             assert response.status_code == status.HTTP_200_OK

# #         assert response.json() == {"permissions": {"vehicles.can_foo": True}}


# # @pytest.mark.django_db
# # def test_get_user_permissions_with_role_permissions(
# #     client, auth_user, role, perm1, perm2
# # ):
# #     role.user_set.add(auth_user)
# #     role.permissions.add(perm2)
# #     with scopes_disabled():
# #         with authenticated_user(auth_user):
# #             response = client.get(reverse("user_has_permissions"))
# #             assert response.status_code == status.HTTP_200_OK

# #         assert response.json() == {"permissions": {"vehicles.can_bar": True}}


# # @pytest.mark.django_db
# # def test_has_user_permissions(client, auth_user, role, perm1, perm2):
# #     role.user_set.add(auth_user)
# #     role.permissions.add(perm2)
# #     auth_user.user_permissions.add(perm1)
# #     with scopes_disabled():
# #         with authenticated_user(auth_user):
# #             data = {
# #                 "permissions": [
# #                     "admin.can_foo",
# #                     "vehicles.can_foo",
# #                     "vehicles.can_bar",
# #                     "vehicles.can_buzz",
# #                 ]
# #             }
# #             response = client.post(
# #                 reverse("user_has_permissions"),
# #                 json.dumps(data),
# #                 content_type="application/json",
# #             )
# #             assert response.status_code == status.HTTP_200_OK

# #     assert response.json() == {
# #         "permissions": {
# #             "admin.can_foo": False,
# #             "vehicles.can_foo": True,
# #             "vehicles.can_bar": True,
# #             "vehicles.can_buzz": False,
# #         }
# #     }


# @pytest.mark.django_db
# def test_get_role_list(client, auth_user, role_factory):
#     role_factory(id=1, name="User")
#     role_factory(id=2, name="Admin")
#     with scopes_disabled():
#         with authenticated_user(auth_user):
#             response = client.get(reverse("role-list"))
#             assert response.status_code == status.HTTP_200_OK

#     assert response.json() == {
#         "count": 2,
#         "next": None,
#         "previous": None,
#         "results": [
#             {"id": 1, "name": "User"},
#             {"id": 2, "name": "Admin"},
#         ],
#     }


# @pytest.mark.django_db
# def test_get_role(client, auth_user, role_factory):
#     role_factory(id=1, name="User")
#     with scopes_disabled():
#         with authenticated_user(auth_user):
#             response = client.get(reverse("role-detail", (1,)))
#             assert response.status_code == status.HTTP_200_OK

#     assert response.json() == {"id": 1, "name": "User"}


# @pytest.mark.django_db
# # def test_get_user_me(client, auth_user, role, perm2):
# def test_get_user_me(client, auth_user, role):
#     role.user_set.add(auth_user)
#     # role.permissions.add(perm2)
#     # force_authenticate(client, user=auth_user) # пытался так

#     with authenticated_user(auth_user):
#         response = client.get("/api/v1/users/me/")
#         assert response.status_code == status.HTTP_200_OK

#     assert response.json() == {
#         "companyId": str(auth_user.company.id),
#         "companyName": str(auth_user.company.name),
#         "email": auth_user.email,
#         "firstName": "",
#         "id": str(auth_user.id),
#         "isActive": True,
#         "lastName": "",
#         "status": Statuses.ACTIVE,
#         "role": None,
#         "phoneNumber": auth_user.phone_number,
#     }


# # @pytest.mark.django_db
# # def test_post_user(client, auth_user, role_factory):
# #     """Замокать from django_rest_passwordreset.signals из сериалаизера."""
# #     auth_user.is_superuser = True
# #     # auth_user.company.name = "test_company"
# #     role_factory(id=3, name="Mission Operator")
# #     data = {
# #         "email": "janedoe@acme.me",
# #         "first_name": "John",
# #         "last_name": "Doe",
# #     }
# #     # assert auth_user == {}
# #     with authenticated_user(auth_user):
# #         response = client.post(
# #             "/api/v1/users/", json.dumps(data), content_type="application/json"
# #         )
# #         assert response.status_code == status.HTTP_201_CREATED
# #     response_json = response.json()
# #     response_json.pop("id")
# #     assert response_json == {
# #         "companyId": str(auth_user.company.id),
# #         "companyName": str(auth_user.company.name),
# #         # "dashboardLinks": [],
# #         "email": "janedoe@acme.me",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "isActive": True,
# #         "phoneNumber": None,
# #         "status": Statuses.ACTIVE,
# #         "role": 3,
# #     }


# @pytest.mark.django_db
# def test_user_list_sort(client, user_factory):
#     user_1 = user_factory(date_joined=datetime.datetime.fromisoformat("2023-01-01"))
#     user_2 = user_factory()
#     user_3 = user_factory(date_joined=datetime.datetime.fromisoformat("2023-05-01"))
#     user_1.is_superuser = True
#     with authenticated_user(user_1):
#         response = client.get(reverse("user-list"))
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert "results" in data
#     assert len(data["results"]) == 3
#     assert data["results"][0]["id"] == str(user_2.id)
#     assert data["results"][1]["id"] == str(user_3.id)
#     assert data["results"][2]["id"] == str(user_1.id)
