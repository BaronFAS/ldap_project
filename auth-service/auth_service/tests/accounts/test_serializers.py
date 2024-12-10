# import json
# import uuid

# import pytest
# from accounts.models import Role, Statuses, User
# from django.core.management import call_command
# from django_scopes import scopes_disabled
# from rest_framework.reverse import reverse
# from tests.auth import authenticated_user


# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     # Initialize roles and permissions prior running the test case
#     with django_db_blocker.unblock():
#         # call_command("create_roles")
#         call_command("createrole", "Viewer")
#         # call_command("createrole", "Admin")


# @pytest.fixture
# def company1(company_factory):
#     return company_factory()


# @pytest.fixture
# def company2(company_factory):
#     return company_factory()


# @pytest.fixture
# def user1(user_factory, company1):
#     return user_factory(
#         id=uuid.UUID(int=1),
#         email="johndoe@acme.me",
#         phone_number="+18396901266",
#         first_name="John",
#         last_name="Doe",
#         company=company1,
#     )


# # @pytest.fixture
# # def dashboard_link1(dashboard_links_factory):
# #     return dashboard_links_factory()


# def create_user_with_role(user_factory, company, role):
#     user = user_factory(company=company)

#     role = Role.objects.get(name=role)
#     role.user_set.add(user)

#     return user


# @pytest.mark.django_db
# # def test_view_user_as_viewer(client, user_factory, company1, user1, dashboard_link1):
# def test_view_user_as_viewer(client, user_factory, company1, user1):
#     """Проходит тесты если передавать Роль аналогичную 'call_command("createrole", "Viewer")'."""
#     # viewer = create_user_with_role(user_factory, company1, "Default Role")
#     viewer = create_user_with_role(user_factory, company1, "Viewer")

#     with authenticated_user(viewer):
#         response = client.get(reverse("user-detail", (user1.id,)))
#         assert response.status_code == 200

#     assert response.json() == {
#         "companyId": str(company1.id),
#         "companyName": company1.name,
#         # "dashboardLinks": [],
#         # "id": None,
#         # "id": '00000000-0000-0000-0000-000000000001',
#         "id": '00000000-0000-0000-0000-000000000001',
#         "email": "johndoe@acme.me",
#         "phoneNumber": "+18396901266",
#         "firstName": "John",
#         "lastName": "Doe",
#         "status": Statuses.ACTIVE,
#         "role": None,
#         "isActive": None,
#         # "image": None,
#     }


# # @pytest.mark.django_db
# # def test_view_user_as_admin(client, user_factory, company1, user1):
# #     """Тут надо разбиратся нужена ли нам Роль Admin."""
# #     admin = create_user_with_role(user_factory, company1, "Admin")

# #     with authenticated_user(admin):
# #         response = client.get(reverse("user-detail", (user1.id,)))
# #         assert response.status_code == 200

# #     assert response.json() == {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         # "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "johndoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "status": Statuses.ACTIVE,
# #         "role": None,
# #         "isActive": True,
# #         # "image": None,
# #     }


# # @pytest.mark.django_db
# # def test_view_user_as_super_admin(client, user_factory, company1, user1):
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     with authenticated_user(super_admin):
# #         response = client.get(reverse("user-detail", (user1.id,)))
# #         assert response.status_code == 200

#     # assert response.json() == {
#     #     "companyId": str(company1.id),
#     #     "companyName": company1.name,
#     #     # "dashboardLinks": [],
#     #     "id": "00000000-0000-0000-0000-000000000001",
#     #     "phoneNumber": "+18396901266",
#     #     "email": "johndoe@acme.me",
#     #     "firstName": "John",
#     #     "lastName": "Doe",
#     #     "status": Statuses.ACTIVE,
#     #     "role": None,
#     #     "isActive": True,
#     #     # "image": None,
#     # }


# # @pytest.mark.django_db
# # def test_create_user(client, user_factory, company1):
# #     default_role, _ = Role.objects.get_or_create(name="Mission Operator")
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         "dashboardLinks": [],
# #         "email": "johndoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #     }

# #     with authenticated_user(super_admin):
# #         response = client.post(
# #             reverse("user-list"),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 201

# #     response_json = response.json()
# #     user_id = response_json.pop("id")
# #     assert response_json == {
# #         "companyId": str(company1.id),
# #         "companyName": str(company1.name),
# #         # "dashboardLinks": [],
# #         "email": "johndoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "status": Statuses.ACTIVE,
# #         "role": default_role.id,
# #         "isActive": True,
# #     }

# #     with scopes_disabled():
# #         user = User.objects.get(id=user_id)
# #     assert user.role
# #     assert user.role_id == default_role.id


# # @pytest.mark.django_db
# # def test_create_user_with_role(client, user_factory, company1):
# #     viewer_role, _ = Role.objects.get_or_create(name="Viewer")
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "companyId": str(company1.id),
# #         "email": "johndoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "isActive": False,
# #         "role": viewer_role.id,
# #     }

# #     with authenticated_user(super_admin):
# #         response = client.post(
# #             reverse("user-list"),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 201

# #     response_json = response.json()
# #     response_json.pop("id")
# #     assert response_json == {
# #         "companyId": str(company1.id),
# #         "companyName": str(company1.name),
# #         # "dashboardLinks": [],
# #         "email": "johndoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "status": Statuses.ACTIVE,
# #         "role": viewer_role.id,
# #         "isActive": True,  # all users are active when created
# #         }


# # @pytest.mark.django_db
# # def test_update_user(client, user_factory, company1, user1):
# #     viewer_role = Role.objects.get(name="Viewer")
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "janedoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "Jane",
# #         "lastName": "Doe",
# #         "isActive": True,
# #         "role": viewer_role.id,
# #     }

# #     client.force_login(user1)

# #     # update user
# #     with authenticated_user(super_admin):
# #         response = client.put(
# #             reverse("user-detail", (str(user1.id),)),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 200

# #     response_json = response.json()
# #     assert response_json == {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "janedoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "Jane",
# #         "lastName": "Doe",
# #         "status": Statuses.ACTIVE,
# #         "role": viewer_role.id,
# #         "isActive": True,
# #     }


# # @pytest.mark.django_db
# # def test_update_status_user(client, user_factory, company1, user1):
# #     viewer_role = Role.objects.get(name="Viewer")
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         # "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "janedoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "Jane",
# #         "lastName": "Doe",
# #         "status": Statuses.INACTIVE,
# #         "role": viewer_role.id,
# #     }

# #     client.force_login(user1)

# #     # update user
# #     with authenticated_user(super_admin):
# #         response = client.put(
# #             reverse("user-detail", (str(user1.id),)),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 200

# #     response_json = response.json()
# #     assert response_json == {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         # "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "janedoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "Jane",
# #         "lastName": "Doe",
# #         "status": Statuses.INACTIVE,
# #         "role": viewer_role.id,
# #         "isActive": False,
# #     }


# # @pytest.mark.django_db
# # def test_update_status_user_admin(client, user_factory, company1, user1):
# #     admin = create_user_with_role(user_factory, company1, "Admin")

# #     user_data = {
# #         "email": "janedoe@acme.me",
# #         "status": Statuses.INACTIVE,
# #     }

# #     with authenticated_user(admin):
# #         response = client.put(
# #             reverse("user-detail", (str(user1.id),)),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 200

# #     response_json = response.json()
# #     assert "status" in response_json
# #     assert response_json["status"] == Statuses.INACTIVE

# #     new_user_data = {
# #         "email": "janedoe@acme.me",
# #         "status": "jibberish",
# #     }

# #     with authenticated_user(admin):
# #         response = client.put(
# #             reverse("user-detail", (str(user1.id),)),
# #             json.dumps(new_user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 400
# #         response_json = response.json()
# #         assert "detail" in response_json
# #         assert "Field: status." in response_json["detail"]


# @pytest.mark.django_db
# def test_update_status_user_wo_permissions(
#     client, user_factory, company1, user1
# ):
#     viewer_role = Role.objects.get(name="Viewer")
#     not_admin = create_user_with_role(user_factory, company1, viewer_role)

#     user_data = {
#         "companyId": str(company1.id),
#         "companyName": company1.name,
#         # "dashboardLinks": [],
#         "id": str(user1.id),
#         "email": "janedoe@acme.me",
#         "phoneNumber": "+18396901266",
#         "firstName": "Jane",
#         "lastName": "Doe",
#         "status": Statuses.INACTIVE,
#         "role": viewer_role.id,
#     }

#     # update user
#     with authenticated_user(not_admin):
#         response = client.put(
#             reverse("user-detail", (str(user1.id),)),
#             json.dumps(user_data),
#             content_type="application/json",
#         )
#         assert response.status_code == 403


# # @pytest.mark.django_db
# # def test_update_user_company_id_super_admin(client, user_factory, company1, company2):
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "companyId": str(company2.id),
# #     }

# #     # update user
# #     with authenticated_user(super_admin):
# #         response = client.patch(
# #             reverse("user-detail", (str(super_admin.id),)),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 200

# #     response_json = response.json()
# #     assert response_json["companyId"] == str(company2.id)


# @pytest.mark.django_db
# def test_update_user_company_id_viwer(client, user_factory, company1, company2):
#     super_admin = create_user_with_role(user_factory, company1, "Viewer")

#     user_data = {
#         "companyId": str(company2.id),
#     }

#     # update user
#     with authenticated_user(super_admin):
#         response = client.patch(
#             reverse("user-detail", (str(super_admin.id),)),
#             json.dumps(user_data),
#             content_type="application/json",
#         )
#         assert response.status_code == 403


# # @pytest.mark.django_db
# # def test_partially_update_user(client, user_factory, company1, user1):
# #     editor_role = Role.objects.get(name="Editor")
# #     super_admin = create_user_with_role(user_factory, company1, "Super Admin")

# #     user_data = {
# #         "email": "janedoe@acme.me",
# #         "role": editor_role.id,
# #     }

# #     client.force_login(user1)

# #     # update user
# #     with authenticated_user(super_admin):
# #         response = client.patch(
# #             reverse("user-detail", (str(user1.id),)),
# #             json.dumps(user_data),
# #             content_type="application/json",
# #         )
# #         assert response.status_code == 200

# #     response_json = response.json()
# #     assert response_json == {
# #         "companyId": str(company1.id),
# #         "companyName": company1.name,
# #         "dashboardLinks": [],
# #         "id": str(user1.id),
# #         "email": "janedoe@acme.me",
# #         "phoneNumber": "+18396901266",
# #         "firstName": "John",
# #         "lastName": "Doe",
# #         "status": Statuses.ACTIVE,
# #         "role": editor_role.id,
# #         "isActive": True,
# #         },
# #     }


# # @pytest.mark.django_db
# # class TestPartialUpdateUserPermissions:
# #     @pytest.fixture()
# #     def other_user(self, user_factory, company):
# #         yield create_user_with_role(user_factory, company, "Editor")

# #     @pytest.fixture(
# #         params=[
# #             ("companyId", None),
# #             ("companyName", None),
# #             ("email", "janedoe@acme.me"),
# #             ("phoneNumber", "+18396901266"),
# #             ("firstName", "John"),
# #             ("lastName", "Doe"),
# #             ("isActive", True),
# #             # ("image", None),
# #         ],
# #     )
# #     def user_data(self, request, company):
# #         field_name, value = request.param
# #         if field_name == "companyId":
# #             value = str(company.id)

# #         if field_name == "companyName":
# #             value = company.name

# #         return {field_name: value}

# #     def test_update_for_super_admin(
# #         self, client, user_factory, company, user_data, other_user
# #     ):
# #         user = create_user_with_role(user_factory, company, "Super Admin")

# #         with authenticated_user(user):
# #             response = client.patch(
# #                 reverse("user-detail", (str(other_user.id),)),
# #                 json.dumps(user_data),
# #                 content_type="application/json",
# #             )
# #             assert response.status_code == 200

# #     def test_update_for_admin(
# #         self, client, user_factory, company, user_data, other_user
# #     ):
# #         user = create_user_with_role(user_factory, company, "Admin")

# #         with authenticated_user(user):
# #             response = client.patch(
# #                 reverse("user-detail", (str(other_user.id),)),
# #                 json.dumps(user_data),
# #                 content_type="application/json",
# #             )
# #             assert response.status_code == 200

# #     @pytest.mark.parametrize(
# #         "role",
# #         [
# #             "Viewer",
# #             "Vehicle Operator",
# #             "Mission Operator",
# #             "Remote Control Operator",
# #             "User",
# #             "Editor",
# #         ],
# #     )
# #     def test_update_for_other_roles(
# #         self, client, user_factory, company, user_data, other_user, role
# #     ):
# #         user = create_user_with_role(user_factory, company, role)

# #         fields_for_change = set(user_data.keys())
# #         assert len(fields_for_change) == 1, "Only one key for update model"
# #         field = fields_for_change.pop()

# #         with authenticated_user(user):
# #             response = client.patch(
# #                 reverse("user-detail", (str(user.id),)),
# #                 json.dumps(user_data),
# #                 content_type="application/json",
# #             )
# #             assert response.status_code == 200 if field in {"image"} else 403

# #             response = client.patch(
# #                 reverse("user-detail", (str(other_user.id),)),
# #                 json.dumps(user_data),
# #                 content_type="application/json",
# #             )
# #             assert response.status_code == 403
