from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import include, path, re_path
from rest_framework import routers, permissions

from external_services.views import (
    UserViewSetExternal,
    RoleViewSetExternal,
    CompanyViewSetExternal,
)


app_name = "external_services"
router = routers.DefaultRouter()
router.register(r"users", UserViewSetExternal, basename='user')
router.register(r"roles", RoleViewSetExternal, basename='role')
router.register(r"companies", CompanyViewSetExternal, basename='company')

schema_view_external = get_schema_view(
    openapi.Info(
        title="API external_services",
        default_version="external_services v2",
        description=(
            "To use the api, get a jwt token in the admin panel and add "
            "{'JWT-Custom-Header': your_token} to the HTTP request."
        ),
    ),
    patterns=[
        path("api/v2/external_services/", include(router.urls)),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("v2/external_services/", include(router.urls)),
    re_path(
        r"^v2/external_services/docs/$",
        schema_view_external.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui-external",
    ),
]
