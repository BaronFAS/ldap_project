import jwt
import logging

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from external_services.serializers import (
    UserSerializerExternal,
    RoleSerializerExternal,
    CompanySerializerExternal
)
from accounts.models import Role, User
from external_services.models import Services
from companies.models import Company
from auth_service.config import SECRET_KEY_SERVICE
from accounts.utils import LDAPManager


logger = logging.getLogger(__name__)


class JWTAuthViewSetMixin:
    """A mixin that checks for the presence of a
    custom JWT token in the request header."""
    def check_jwt_token(self, request):
        key = request.headers.get("JWT-Custom-Header", None)
        logging.info(f"Key: {key}")
        if not key:
            return JsonResponse(
                {"error": "Requires JWT token from admin panel!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            payload = jwt.decode(key, SECRET_KEY_SERVICE, algorithms=['HS256'])
            logging.info(f"JWT token: {payload}")
            Services.objects.get(service_name=payload["service_name"])
            return payload
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {'error': 'Token has expired'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return JsonResponse(
                {'error': 'Invalid token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Services.DoesNotExist:
            return JsonResponse(
                {'error': 'Service not found'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSetExternal(
    JWTAuthViewSetMixin,
    viewsets.ReadOnlyModelViewSet
):
    """Endpoint for obtaining a list of users and user by id.
    Attention, for use you need to obtain a JWT token in the
    admin panel in the Services section. Add the header
    "JWT-Custom-Header" with your token to the http request.
    For example: {"JWT-Custom-Header": your_token}."""
    serializer_class = UserSerializerExternal
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        if user.is_authenticated and hasattr(user, 'company'):
            return User.objects.filter(
                Q(company=user.company) | Q(company__isnull=True)
            )

        return User.objects.none()


    def list(self, request):
        # для суперюзеров
        # user = request.user
        # if user.is_superuser:
        #     queryset = self.get_queryset()
        #     serializer = self.serializer_class(queryset, many=True)
        #     return Response(serializer.data)
        # logging.info(f"Request data: {request.data}")
        # logging.info(f"Request query params: {request.query_params}")
        # logging.info(f"Request user: {request.user}")
        # jwt_token = request.headers.get("JWT-Custom-Header", None)
        # logging.info(f"JWT token: {jwt_token}")

        payload = self.check_jwt_token(request)
        if isinstance(payload, JsonResponse):
            return payload
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class RoleViewSetExternal(
    JWTAuthViewSetMixin,
    viewsets.ReadOnlyModelViewSet
):
    """Endpoint for obtaining a list of roles and role by id.
    Attention, for use you need to obtain a JWT token in the
    admin panel in the Services section. Add the header
    "JWT-Custom-Header" with your token to the http request.
    For example: {"JWT-Custom-Header": your_token}."""
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializerExternal
    permission_classes = [IsAuthenticated]

    def list(self, request):
        payload = self.check_jwt_token(request)
        if isinstance(payload, JsonResponse):
            return payload
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CompanyViewSetExternal(
    JWTAuthViewSetMixin,
    viewsets.ReadOnlyModelViewSet
):
    """Endpoint for obtaining a list of companies and companies by id.
    Attention, for use you need to obtain a JWT token in the
    admin panel in the Services section. Add the header
    "JWT-Custom-Header" with your token to the http request.
    For example: {"JWT-Custom-Header": your_token}."""
    serializer_class = CompanySerializerExternal
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Company.objects.all().order_by("id")

        if user.is_authenticated:
            if not user.company:
                return Company.objects.none()
            return Company.objects.filter(user=user)

        return Company.objects.none()

    def list(self, request):
        payload = self.check_jwt_token(request)
        if isinstance(payload, JsonResponse):
            return payload
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
