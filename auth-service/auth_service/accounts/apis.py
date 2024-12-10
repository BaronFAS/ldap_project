import logging

from rest_framework import permissions
from rest_framework import serializers
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from utils import renderers
from api.mixins import ApiAuthMixin
from api.mixins import ApiErrorsMixin
from api.mixins import PublicApiMixin
# from auth.services import google_validate_id_token
from accounts.services import user_get_or_create
from accounts.selectors import get_user_permissions
from accounts.serializers import UserSerializer


logger = logging.getLogger(__name__)


class UserMeApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    http_method_names = ["get"]
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.CamelCaseJSONRenderer]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = UserSerializer(user, context={"request": request}).data
        return Response(data)


class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False, default="")
        last_name = serializers.CharField(required=False, default="")

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get("Authorization")
        # google_validate_id_token(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _ = user_get_or_create(**serializer.validated_data)

        if user.is_active:
            refresh = RefreshToken.for_user(user)
            response = Response(
                data={
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            )
        else:
            response = Response(data={})
        if user.is_superuser:
            login(request, user)
        else:
            # flush the session to avoid using another user's session
            request.session.flush()

        return response


class UserPermissionsApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    http_method_names = ["get", "post"]
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        has_permissions = {}
        for permission in request.user.get_group_permissions():
            has_permissions[permission] = True
        for permission in request.user.get_user_permissions():
            has_permissions[permission] = True

        return Response({"permissions": has_permissions})

    def post(self, request, *args, **kwargs):
        permissions = request.data.get("permissions", [])
        has_permissions = get_user_permissions(permissions, request.user)
        return Response({"permissions": has_permissions})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error("User status not update error: {}".format(e))
        return response
