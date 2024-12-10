from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import include, path, re_path
from rest_framework import routers, permissions

from accounts.views import UserViewSetV2, RoleViewSetV2
from accounts.admin import ServicesAdmin
from companies.views import CompanyViewSet2


app_name = "accounts"
router = routers.DefaultRouter()


router.register(r"users", UserViewSetV2, basename='user')
router.register(r"roles", RoleViewSetV2, basename='role')

router_companies = routers.DefaultRouter()
router_companies.register(r"companies", CompanyViewSet2, basename='company')

schema_view = get_schema_view(
    openapi.Info(
        title="Cloud-Core API",
        default_version="v2",
        description="cloude-core api",
    ),
    patterns=[
        path("api/v2/", include(router.urls)),
        path("api/v2/", include(router_companies.urls)),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("v2/", include(router.urls)),
    path("v2/", include(router_companies.urls)),
    path(
        '<int:pk>/regenerate-token/',
        ServicesAdmin.regenerate_token_view,
        name='services_regenerate_token'
    ),
    re_path(
        r"^v2/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
