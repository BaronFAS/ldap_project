import logging

from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import renderers
from accounts.models import Role, User
from accounts.serializers import (
    RoleSerializer,
    UserSerializer,
    UserSerializerV2,
    UserPostUpdateSerializerV2,
    RoleSerializerV2
)
from accounts.permissions import IsCompanyAdminOrSuperuser
from accounts.utils import LDAPManager


logger = logging.getLogger(__name__)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Roles API endpoint.
    """

    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint Users.
    """

    queryset = User.objects.none()
    serializer_class = UserSerializer
    renderer_classes = [
        renderers.CamelCaseJSONRenderer,
        renderers.CamelCaseBrowsableAPIRenderer,
        renderers.JSONRenderer,
    ]

    def get_permissions(self):
        return [permissions.AllowAny()]
        # if self.request.method == "PATCH":
        #     return [permissions.IsAuthenticated()]
        # else:
        #     return [permissions.DjangoModelPermissions()]

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class UserViewSetV2(viewsets.ModelViewSet):
    """API endpoint Users."""

    serializer_class = UserSerializerV2
    permission_classes = [IsAuthenticated, IsCompanyAdminOrSuperuser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializerV2
        return UserPostUpdateSerializerV2

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        if user.is_authenticated and hasattr(user, 'company'):
            return User.objects.filter(
                Q(company=user.company) | Q(company__isnull=True)
            )

        return User.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Start deleting user from LDAP
        with LDAPManager() as ldap_manager:
            ldap_manager.delete_user_by_uid(instance.id)
        # End deleting user from LDAP

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleViewSetV2(viewsets.ModelViewSet):
    """Roles API V2 endpoint."""
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializerV2
    permission_classes = [IsAuthenticated]
