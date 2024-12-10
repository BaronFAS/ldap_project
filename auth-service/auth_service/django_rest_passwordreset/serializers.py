import logging
from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework import serializers
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_rest_passwordreset import models
from django_rest_passwordreset.models import get_password_reset_token_expiry_time


logger = logging.getLogger(__name__)


__all__ = [
    "EmailSerializer",
    "PasswordTokenSerializer",
    "ResetTokenSerializer",
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordValidateMixin:
    def validate(self, data):
        token = data.get("token")

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()
        # find token
        try:
            reset_password_token = _get_object_or_404(models.ResetPasswordToken, key=token)
        except (
            TypeError,
            ValueError,
            ValidationError,
            Http404,
            models.ResetPasswordToken.DoesNotExist,
        ):
            error = _("The OTP password entered is not valid. Please check and try again.")
            logging.warning(error)
            raise ValidationError(error)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            error = _("The token has expired")
            logging.warning(error)
            raise ValidationError(error)
        return data


class PasswordTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={"input_type": "password"})
    token = serializers.CharField()


class ResetTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    token = serializers.CharField()
