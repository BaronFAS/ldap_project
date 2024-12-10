import jwt
import datetime as dt

from django import forms

from external_services.models import Services
from auth_service.config import (
    SECRET_KEY_SERVICE,
    JWT_TOKEN_EXTERNAL_SERVICES,
)


class ServicesForm(forms.ModelForm):
    """Form for creating a jwt token through the admin panel."""
    class Meta:
        model = Services
        fields = ["service_name", "service_url"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        exp_datetime = dt.datetime.utcnow() + dt.timedelta(
            days=JWT_TOKEN_EXTERNAL_SERVICES
        )
        payload = {
            "service_name": instance.service_name,
            "exp": exp_datetime,
            "iat": dt.datetime.utcnow(),
        }
        secret_key = SECRET_KEY_SERVICE
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        instance.jwt_token = token
        if commit:
            instance.save()
        return instance
