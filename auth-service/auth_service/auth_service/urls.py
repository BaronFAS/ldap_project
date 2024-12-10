from drf_yasg import openapi
from django.conf import settings
from django.urls import path
from django.urls import include
from django.urls import re_path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework import permissions
# from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from api.views import JWTGenerateView
from accounts.apis import UserMeApi
from accounts.apis import UserInitApi
from accounts.apis import UserPermissionsApi
from accounts.apis import CustomTokenObtainPairView
from accounts.views import RoleViewSet
from accounts.views import UserViewSet
from companies.views import CompanyViewSet


router = routers.DefaultRouter()
router.register(r"companies", CompanyViewSet)
# router.register(r"sites", SiteViewSet)
# router.register(r"fleets/mission_queue", FleetQueueMissionsViewSet)
# router.register(r"fleets", FleetViewSet)
# router.register(r"vehicle_types", VehicleTypeViewSet)
# router.register(r"vehicle_configurations", VehicleConfigurationViewSet)
# router.register(r"vehicles", VehicleViewSet)
# router.register(r"localization_maps", LocalizationMapViewSet)
# router.register(r"semantic_maps", SemanticMapViewSet)
# router.register(
#     r"missions/operator_flow",
#     MissionOperatorFlowViewSet,
#     basename="mission-operator-flow",
# )
# router.register(r"missions", MissionViewSet)
# router.register(r"missions_queue", MissionQueueViewSet)
# router.register(r"stops", StopViewSet)
router.register(r"roles", RoleViewSet)
router.register(r"users", UserViewSet)
# router.register(r"mission_deployment", DeploymentViewSet)
# router.register(r"vehicle_deployment", VehicleDeploymentViewSet)
# router.register(r"bulk", BulkLoadViewSet, basename="bulk")


schema_view = get_schema_view(
    openapi.Info(
        title="Cloud-Core API",
        default_version="v1",
        description="cloude-core api",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger
    # TODO it is necessary to redo the formation of urls and add on/off switch for Swagger
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    path('api/', include('accounts.urls', namespace='accounts')),
    # path('api/', include('companies.urls', namespace='companies')),
    path('api/', include(
        'external_services.urls',
        namespace='external_services'
        )),
    re_path(
        r"^api/v1/docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/v1/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # Urls
    # path("api/v1/admin/", include("loginas.urls")),
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/v1/login/GoogleOauth2/",
        UserInitApi.as_view(),
        name="token_obtain_pair_google_oauth_2",
    ),
    path("api/v1/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/api-auth/", include("rest_framework.urls")),
    path(
        "api/v1/users/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/v1/users/me/", UserMeApi.as_view(), name="me"),
    path("api/v1/users/init/", UserInitApi.as_view(), name="init"),
    path(
        "api/v1/users/has-permissions/",
        UserPermissionsApi.as_view(),
        name="user_has_permissions",
    ),
    # path("api/v1/feature_flags/", FeatureFlagsV2ViewSet.as_view(), name="feature flags v2"),
    # path(
    #     "api/v1/vehicles/<uuid:vehicle_id>/registration/",
    #     VehicleRegistrationView.as_view(),
    #     name="vehicle-registration-edit",
    # ),
    # path("api/v1/vehicles/registration/", VehicleRegistrationView.as_view(), name="vehicle-registration"),
    path("api/v1/", include(router.urls)),
    # path(
    #     "api/v1/vehicles_state_query/",
    #     VehicleStatusViewSet.as_view(),
    #     name="vehicles_state_query",
    # ),
    path("api/v1/jwt/generate/", JWTGenerateView.as_view(), name="jwt-generate"),
    # path("api/v1/upload-bulk", FileUploadView.as_view(), name="upload-bulk"),
    # path("api/v1/", include("waffle.urls")),
    # path("", include("django_prometheus.urls")),
    # path("", include("healthcheck.urls")),
    # path("api/v1/", include("healthcheck.urls")),
    # path("api/v1/", include("assets.urls")),
    # path("api/v1/live_missions/", LiveMissionViewSet.as_view({"get": "list"}), name="livemissions"),
]


# vehicle_router = NestedSimpleRouter(router, r"vehicles", lookup="vehicle")
# vehicle_router.register(r"mission_queue", VehicleQueueMissionsViewSet, basename="mission_queue")

# urlpatterns += [
#     path(r"api/v1/", include(vehicle_router.urls)),
# ]

# if settings.STATIC_SERVE_BY_APP:
#     urlpatterns += staticfiles_urlpatterns()

# if settings.MISSION_OPERATOR_EMULATION_ENABLED:
#     urlpatterns.append(
#         path(
#             "api/v1/mission_operator_emulate_ws_message/",
#             MissionOperatorEmulateView.as_view(),
#             name="mission_operator_emulate_ws_message",
#         ),
#     )

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
