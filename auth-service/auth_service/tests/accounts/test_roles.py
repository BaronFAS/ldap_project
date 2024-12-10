# import json

# import pytest
# from accounts.models import Role
# from django.core.management import call_command
# from rest_framework import status
# from rest_framework.reverse import reverse
# from tests.auth import authenticated_user

# # fmt: off

# # This object contains test parameters for parameterized test cases
# # In order to reduce size of the configuration the same config
# # contains parameters for create/update/delete test cases
# # The only difference between these tests is the returned HTTP code.
# test_parameters = (
#     "path,get_http_code,update_http_code,delete_http_code,role,company,object",
#     [
#         # delete User in my company
#         ("user-detail", 200, 403, 403, "Default Role", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "Viewer", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "Mission Operator", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "User", "my_company", "my_user"),
#         # ("user-detail", 200, 403, 403, "Editor", "my_company", "my_user"),
#         # ("user-detail", 200, 415, 204, "Admin", "my_company", "my_user"),
#         # ("user-detail", 200, 415, 204, "Super Admin", "my_company", "my_user"),

#         # delete User in other company
#         # ("user-detail", 404, 404, 404, "Admin", "my_company", "other_user"),
#         # ("user-detail", 200, 415, 204, "Super Admin", "my_company", "other_user"),

#         # delete Company in my company
#         # ("company-detail", 200, 403, 403, "Viewer", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "Mission Operator", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "User", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "Editor", "my_company", "my_company"),
#         # ("company-detail", 200, 403, 403, "Admin", "my_company", "my_company"),
#         # ("company-detail", 200, 415, 204, "Super Admin", "my_company", "my_company"),

#         # delete Company in other company
#         # ("company-detail", 200, 415, 204, "Super Admin", "my_company", "other_company"),

#         # delete Fleet in my company
#         # ("fleet-detail", 200, 403, 403, "Viewer", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 403, 403, "Mission Operator", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 415, 204, "User", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 415, 204, "Editor", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 415, 204, "Admin", "my_company", "my_fleet"),
#         # ("fleet-detail", 200, 415, 204, "Super Admin", "my_company", "my_fleet"),

#         # delete Fleet in other company
#         # ("fleet-detail", 404, 404, 404, "User", "my_company", "other_fleet"),
#         # ("fleet-detail", 404, 404, 404, "Editor", "my_company", "other_fleet"),
#         # ("fleet-detail", 404, 404, 404, "Admin", "my_company", "other_fleet"),
#         # ("fleet-detail", 200, 415, 204, "Super Admin", "my_company", "other_fleet"),

#         # delete LocalizationMap in my company
#         # ("localizationmap-detail", 200, 403, 403, "Viewer", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 403, 403, "Mission Operator", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 415, 204, "User", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 415, 204, "Editor", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 415, 204, "Admin", "my_company", "my_localization_map"),
#         # ("localizationmap-detail", 200, 415, 204, "Super Admin", "my_company", "my_localization_map"),

#         # delete LocalizationMap in other company
#         # ("localizationmap-detail", 404, 404, 404, "User", "my_company", "other_localization_map"),
#         # ("localizationmap-detail", 404, 404, 404, "Editor", "my_company", "other_localization_map"),
#         # ("localizationmap-detail", 404, 404, 404, "Admin", "my_company", "other_localization_map"),
#         # ("localizationmap-detail", 200, 415, 204, "Super Admin", "my_company", "other_localization_map"),

#         # delete SemanticMap in my company
#         # ("semanticmap-detail", 200, 403, 403, "Viewer", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 403, 403, "Mission Operator", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 415, 204, "User", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 415, 204, "Editor", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 415, 204, "Admin", "my_company", "my_semantic_map"),
#         # ("semanticmap-detail", 200, 415, 204, "Super Admin", "my_company", "my_semantic_map"),

#         # delete SemanticMap in other company
#         # ("semanticmap-detail", 404, 404, 404, "User", "my_company", "other_semantic_map"),
#         # ("semanticmap-detail", 404, 404, 404, "Editor", "my_company", "other_semantic_map"),
#         # ("semanticmap-detail", 404, 404, 404, "Admin", "my_company", "other_semantic_map"),
#         # ("semanticmap-detail", 200, 415, 204, "Super Admin", "my_company", "other_semantic_map"),

#         # delete Mission in my company
#         # ("mission-detail", 200, 403, 403, "Viewer", "my_company", "my_mission"),
#         # ("mission-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "Mission Operator", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "Remote Control Operator", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "User", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "Editor", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "Admin", "my_company", "my_mission"),
#         # ("mission-detail", 200, 415, 204, "Super Admin", "my_company", "my_mission"),

#         # delete Mission in other company
#         # ("mission-detail", 404, 404, 404, "Mission Operator", "my_company", "other_mission"),
#         # ("mission-detail", 404, 404, 404, "Remote Control Operator", "my_company", "other_mission"),
#         # ("mission-detail", 404, 404, 404, "User", "my_company", "other_mission"),
#         # ("mission-detail", 404, 404, 404, "Editor", "my_company", "other_mission"),
#         # ("mission-detail", 404, 404, 404, "Admin", "my_company", "other_mission"),
#         # ("mission-detail", 200, 415, 204, "Super Admin", "my_company", "other_mission"),

#         # delete Stop in my company
#         # ("stop-detail", 200, 403, 403, "Viewer", "my_company", "my_stop"),
#         # ("stop-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_stop"),
#         # ("stop-detail", 200, 403, 403, "Mission Operator", "my_company", "my_stop"),
#         # ("stop-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_stop"),
#         # ("stop-detail", 200, 415, 204, "User", "my_company", "my_stop"),
#         # ("stop-detail", 200, 415, 204, "Editor", "my_company", "my_stop"),
#         # ("stop-detail", 200, 415, 204, "Admin", "my_company", "my_stop"),
#         # ("stop-detail", 200, 415, 204, "Super Admin", "my_company", "my_stop"),

#         # delete Stop in other company
#         # ("stop-detail", 404, 404, 404, "User", "my_company", "other_stop"),
#         # ("stop-detail", 404, 404, 404, "Editor", "my_company", "other_stop"),
#         # ("stop-detail", 404, 404, 404, "Admin", "my_company", "other_stop"),
#         # ("stop-detail", 200, 415, 204, "Super Admin", "my_company", "other_stop"),

#         # delete Vehicle in my company
#         # ("vehicle-detail", 200, 403, 403, "Viewer", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 403, 403, "Vehicle Operator", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 403, 403, "Mission Operator", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 403, 403, "Remote Control Operator", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 415, 204, "User", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 415, 204, "Editor", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 415, 204, "Admin", "my_company", "my_vehicle"),
#         # ("vehicle-detail", 200, 415, 204, "Super Admin", "my_company", "my_vehicle"),

#         # delete Vehicle in other company
#         # ("vehicle-detail", 404, 404, 404, "User", "my_company", "other_vehicle"),
#         # ("vehicle-detail", 404, 404, 404, "Editor", "my_company", "other_vehicle"),
#         # ("vehicle-detail", 404, 404, 404, "Admin", "my_company", "other_vehicle"),
#         # ("vehicle-detail", 200, 415, 204, "Super Admin", "my_company", "other_vehicle"),
#     ]
# )


# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     """Что бы заработало надо переделать команду createrole на ввод без input."""
#     # Initialize roles and permissions prior running the test case
#     with django_db_blocker.unblock():
#         # call_command("create_roles")
#         call_command("createrole")


# @pytest.fixture
# def test_models(company_factory, user_factory):
# # def test_models(company_factory, user_factory, site_factory, fleet_factory,
# #                 localization_map_factory, semantic_map_factory,
# #                 mission_factory, stop_factory, vehicle_factory):
#     """
#     This fixture returns a map of objects keyed by object name. These objects
#     can further be used in create/update/delete tests.
#     """
#     my_company = company_factory()
#     other_company = company_factory()

#     my_user = user_factory.create(company=my_company)
#     other_user = user_factory.create(company=other_company)

#     # my_site = site_factory.create(company=my_company)
#     # other_site = site_factory.create(company=other_company)

#     # my_localization_map = localization_map_factory.create(site=my_site)
#     # other_localization_map = localization_map_factory.create(site=other_site)

#     # my_semantic_map = semantic_map_factory.create(localization_map=my_localization_map)
#     # other_semantic_map = semantic_map_factory.create(localization_map=other_localization_map)

#     # my_mission = mission_factory.create(semantic_map=my_semantic_map)
#     # other_mission = mission_factory.create(semantic_map=other_semantic_map)

#     # my_stop = stop_factory.create(semantic_map=my_semantic_map)
#     # other_stop = stop_factory.create(semantic_map=other_semantic_map)

#     # my_fleet = fleet_factory.create(site=my_site, semantic_map=my_semantic_map)
#     # other_fleet = fleet_factory.create(site=other_site, semantic_map=other_semantic_map)

#     # my_vehicle = vehicle_factory.create(fleet=my_fleet, company=my_company)
#     # other_vehicle = vehicle_factory.create(fleet=other_fleet, company=other_company)

#     return {
#         "my_company": my_company,
#         "other_company": my_company,
#         "my_user": my_user,
#         "other_user": other_user,
#         # "my_site": my_site,
#         # "other_site": other_site,
#         # "my_localization_map": my_localization_map,
#         # "other_localization_map": other_localization_map,
#         # "my_semantic_map": my_semantic_map,
#         # "other_semantic_map": other_semantic_map,
#         # "my_mission": my_mission,
#         # "other_mission": other_mission,
#         # "my_stop": my_stop,
#         # "other_stop": other_stop,
#         # "my_fleet": my_fleet,
#         # "other_fleet": other_fleet,
#         # "my_vehicle": my_vehicle,
#         # "other_vehicle": other_vehicle,
#     }


# # @pytest.mark.django_db
# # def test_create_roles_command():
# #     """Переписал команду для создания Ролей, но соталась проблема с permissions."""
# #     # viewer = Role.objects.get(name="Viewer")
# #     viewer = Role.objects.get(name="Default Role")
# #     assert viewer.permissions.exists()

#     # vehicle_operator = Role.objects.get(name="Vehicle Operator")
#     # assert vehicle_operator.permissions.exists()

#     # mission_operator = Role.objects.get(name="Mission Operator")
#     # assert mission_operator.permissions.exists()

#     # remote_control_operator = Role.objects.get(name="Remote Control Operator")
#     # assert remote_control_operator.permissions.exists()

#     # user = Role.objects.get(name="User")
#     # assert user.permissions.exists()

#     # editor = Role.objects.get(name="Editor")
#     # assert editor.permissions.exists()

#     # admin = Role.objects.get(name="Admin")
#     # assert admin.permissions.exists()

#     # super_admin = Role.objects.get(name="Super Admin")
#     # assert super_admin.permissions.exists()


# # @pytest.mark.django_db
# # def test_create_roles_force_update_command():
# #     """Аналогично прошлому тесту."""
# #     viewer = Role.objects.get(name="Viewer")
# #     assert viewer.permissions.count() > 0
# #     perm_count = viewer.permissions.count()

# #     viewer.permissions.set([])
# #     assert viewer.permissions.count() == 0

# #     # Call without force-update does not update permissions
# #     call_command("create_roles")
# #     assert viewer.permissions.count() == 0

# #     # Call with force-update updates permissions
# #     call_command("create_roles", "--force-update")
# #     assert viewer.permissions.count() == perm_count


# def create_user_with_role(user_factory, company, role):
#     user = user_factory(company=company)
#     # Make manual adjustments based on the role, users are supposed
#     # to configure this manually in addition to the role
#     if role == "Admin":
#         user.admin = True
#     if role == "Super Admin":
#         user.is_superuser = True

#     role = Role.objects.get(name=role)
#     user.role = role
#     user.save()

#     # assert len(user.get_group_permissions()) > 0

#     return user


# @pytest.mark.parametrize(*test_parameters)
# @pytest.mark.django_db
# def test_get_object(client, user_factory, test_models,
#                     path, get_http_code, update_http_code, delete_http_code, role, company, object):
#     """Не понятно как передать в создание Роли значение не по умолчанию."""
#     company = test_models[company]
#     object = test_models[object]

#     user = create_user_with_role(user_factory, company, role)

#     with authenticated_user(user):
#         response = client.get(reverse(path, (object.id,)))
#         assert response.status_code == get_http_code


# # @pytest.mark.parametrize(*test_parameters)
# # @pytest.mark.django_db
# # def test_update_object(client, user_factory, test_models,
# #                        path, get_http_code, update_http_code, delete_http_code,
# #                        role, company, object):
# #     """Тест возвращает 415. Не понял логику теста."""
# #     company = test_models[company]
# #     object = test_models[object]
# #     user = create_user_with_role(user_factory, company, role)
# #     # update_http_code = 200

# #     with authenticated_user(user):
# #         # There is no need to provide the exact object here, if the user
# #         # has access to the resource, the 415 error will be returned
# #         response = client.put(reverse(path, (object.id,)), data="{}")
# #         assert response.status_code == update_http_code


# # @pytest.mark.parametrize(*test_parameters)
# # @pytest.mark.django_db
# # def test_delete_object(client, user_factory, test_models,
# #                        path, get_http_code, update_http_code, delete_http_code,
# #                        role, company, object):
# #     """Тут аналогично прошлому тесту, только 204."""
# #     company = test_models[company]
# #     object = test_models[object]

# #     user = create_user_with_role(user_factory, company, role)

# #     with authenticated_user(user):
# #         response = client.delete(reverse(path, (object.id,)))
# #         assert response.status_code == delete_http_code


# @pytest.mark.parametrize(
#     "permission,role,has_perm",
#     [
#             ("accounts.view_user_id", "Default Role", False),
# #         ("vehicles.view_remote_control", "Viewer", False),
# #         ("vehicles.view_remote_control", "Vehicle Operator", False),
# #         ("vehicles.view_remote_control", "Mission Operator", False),
# #         ("vehicles.view_remote_control", "Remote Control Operator", False),
# #         ("vehicles.view_remote_control", "User", False),
# #         ("vehicles.view_remote_control", "Editor", False),
# #         ("vehicles.view_remote_control", "Admin", False),
# #         ("vehicles.view_remote_control", "Super Admin", True),

# #         ("vehicles.can_remote_control", "Viewer", False),
# #         ("vehicles.can_remote_control", "Vehicle Operator", False),
# #         ("vehicles.can_remote_control", "Mission Operator", False),
# #         ("vehicles.can_remote_control", "Remote Control Operator", False),
# #         ("vehicles.can_remote_control", "User", False),
# #         ("vehicles.can_remote_control", "Editor", False),
# #         ("vehicles.can_remote_control", "Admin", False),
# #         ("vehicles.can_remote_control", "Super Admin", True),

# #         ("accounts.view_user_is_active", "Viewer", False),
# #         ("accounts.view_user_is_active", "Vehicle Operator", False),
# #         ("accounts.view_user_is_active", "Mission Operator", False),
# #         ("accounts.view_user_is_active", "Remote Control Operator", False),
# #         ("accounts.view_user_is_active", "User", False),
# #         ("accounts.view_user_is_active", "Editor", False),
# #         ("accounts.view_user_is_active", "Admin", True),
# #         ("accounts.view_user_is_active", "Super Admin", True),

#         # ("accounts.view_user_id", "Viewer", False),
# #         ("accounts.view_user_id", "Vehicle Operator", False),
# #         ("accounts.view_user_id", "Mission Operator", False),
# #         ("accounts.view_user_id", "Remote Control Operator", False),
# #         ("accounts.view_user_id", "User", False),
# #         ("accounts.view_user_id", "Editor", False),
# #         ("accounts.view_user_id", "Admin", True),
# #         ("accounts.view_user_id", "Super Admin", True),

# #         ("missions.view_queuedmission", "Viewer", True),
# #         ("missions.view_queuedmission", "Vehicle Operator", True),
# #         ("missions.view_queuedmission", "Mission Operator", True),
# #         ("missions.view_queuedmission", "Remote Control Operator", True),
# #         ("missions.view_queuedmission", "User", True),
# #         ("missions.view_queuedmission", "Editor", True),
# #         ("missions.view_queuedmission", "Admin", True),
# #         ("missions.view_queuedmission", "Super Admin", True),

# #         ("missions.add_queuedmission", "Viewer", False),
# #         ("missions.add_queuedmission", "Vehicle Operator", False),
# #         ("missions.add_queuedmission", "Mission Operator", True),
# #         ("missions.add_queuedmission", "Remote Control Operator", True),
# #         ("missions.add_queuedmission", "User", True),
# #         ("missions.add_queuedmission", "Editor", True),
# #         ("missions.add_queuedmission", "Admin", True),
# #         ("missions.add_queuedmission", "Super Admin", True),

# #         ("missions.change_queuedmission", "Viewer", False),
# #         ("missions.change_queuedmission", "Vehicle Operator", False),
# #         ("missions.change_queuedmission", "Mission Operator", True),
# #         ("missions.change_queuedmission", "Remote Control Operator", True),
# #         ("missions.change_queuedmission", "User", True),
# #         ("missions.change_queuedmission", "Editor", True),
# #         ("missions.change_queuedmission", "Admin", True),
# #         ("missions.change_queuedmission", "Super Admin", True),
#     ]
# )
# @pytest.mark.django_db
# def test_custom_permissions(client, user_factory, permission, role, has_perm):
#     user = create_user_with_role(user_factory, None, role)
#     assert user.has_perm(permission) == has_perm

# # fmt: on


# # @pytest.mark.django_db
# # def test_user_role(
# #     client,
# #     user_factory,
# #     # vehicle,
# #     # mission_factory,
# #     company_factory,
# #     # site_factory,
# #     # localization_map_factory,
# #     # semantic_map_factory,
# # ):
# #     company = company_factory()
# #     # site = site_factory(company=company)
# #     # localization_map = localization_map_factory(site=site)
# #     # semantic_map = semantic_map_factory(localization_map=localization_map)

# #     role_mo = Role.objects.get(name="Mission Operator")
# #     # role_adm = Role.objects.get(name="Admin")
# #     role_viewer = Role.objects.get(name="Viewer")
# #     operator = user_factory(role=role_mo, company=company)
# #     # admin = user_factory(role=role_adm, company=company)
# #     viewer = user_factory(role=role_viewer, company=company)

# #     # mission = mission_factory(semantic_map=semantic_map)

# #     mission_queue_data = {
# #         "name": "Test Mission Name",
# #     }

# #     # with authenticated_user(operator):
# #     #     response = client.patch(
# #     #         reverse("mission-detail", (str(mission.id),)),
# #     #         json.dumps(mission_queue_data),
# #     #         content_type="application/json",
# #     #     )

# #     # assert response.status_code == status.HTTP_200_OK

# #     with authenticated_user(admin):
# #         response = client.patch(
# #             reverse("mission-detail", (str(mission.id),)),
# #             json.dumps(mission_queue_data),
# #             content_type="application/json",
# #         )

# #     assert response.status_code == status.HTTP_200_OK

# #     with authenticated_user(viewer):
# #         response = client.patch(
# #             reverse("mission-detail", (str(mission.id),)),
# #             json.dumps(mission_queue_data),
# #             content_type="application/json",
# #         )

# #     assert response.status_code == status.HTTP_403_FORBIDDEN
