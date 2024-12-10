from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from api.mixins import ApiAuthMixin
from api.mixins import ApiErrorsMixin
from api.mixins import PublicApiMixin
from auth.services import jwt_login
from auth.services import google_validate_id_token
from accounts.services import user_get_or_create
from accounts.selectors import get_my_user


class UserMeApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(get_my_user(user=request.user))


class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False, default="")
        last_name = serializers.CharField(required=False, default="")

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get("Authorization")
        google_validate_id_token(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _ = user_get_or_create(**serializer.validated_data)

        response = Response(data=get_my_user(user=user))
        response = jwt_login(response=response, user=user)

        return response
