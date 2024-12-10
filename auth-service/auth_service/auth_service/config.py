import os
import typing
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


APP_VERSION_LONG = os.getenv("APP_VERSION_LONG", default="0.0.0-fffffff")
APP_VERSION_SHORT = os.getenv("APP_VERSION_SHORT", default="0.0.0")

SECRET_KEY_SERVICE = os.getenv("SECRET_KEY_SERVICE", default="secret_key")
JWT_TOKEN_EXTERNAL_SERVICES = 365 * 10

JWT_EXPIRATION_DELTA_DEFAULT = 2.628e6  # 1 month in seconds
BASE_DIR = Path(__file__).resolve().parent.parent
PHONE_VALIDATE = False


class ServiceSettings(BaseSettings):
    deployment_env: str = Field(env="ENV", default="dev")

    # Django config
    origins: typing.List[str] = ["http://localhost", "http://localhost:3000", "*"]
    secret_key: str = Field(
        env="SECRET_KEY",
        default="django-insecure-x&3mbiof#iz5wx4_#cah&avn7v2ep9h&+e-_(r!mevlt62**a=",
    )
    debug: bool = Field(env="DEBUG", default=False)
    static_serve_by_app: bool = Field(env="STATIC_SERVE_BY_APP", default=True)
    seconds: int = Field(env="DJANGO_JWT_EXPIRATION_DELTA", default=JWT_EXPIRATION_DELTA_DEFAULT)
    static_url: str = Field(env="STATIC_URL", default="/api/v1/static/")
    api_url: str = Field(env="API_URL", default="api/v1")

    # Google api config
    google_oauth2_client_id: str = Field(env="DJANGO_GOOGLE_OAUTH2_CLIENT_ID", default="")
    google_oauth2_client_secret: str = Field(env="DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET", default="")

    # DB config
    db_engine: str = Field(env="POSTGRES_ENGINE", default="django.db.backends.postgresql_psycopg2")
    db_name: str = Field(env="POSTGRES_NAME", default="core_dev")
    db_user: str = Field(env="POSTGRES_USER", default="core_dev")
    db_password: str = Field(env="POSTGRES_PASSWORD", default="")
    db_host: str = Field(env="POSTGRES_HOST", default="")
    db_port: int = Field(env="POSTGRES_PORT", default="5432")

    # Email config
    email_host: str = Field(env="EMAIL_HOST", default="smtp.gmail.com")
    email_use_tls: bool = Field(env="EMAIL_USE_TLS", default=True)
    email_port: int = Field(env="EMAIL_PORT", default=587)
    email_host_user: str = Field(env="EMAIL_HOST_USER", default="no-reply@cyngn.com")
    email_host_password: str = Field(env="EMAIL_HOST_PASSWORD", default="")
    email_sender_display_name: str = Field(env="EMAIL_SENDER_DISPLAY_NAME", default="Cyngn")

    # Password reset config
    password_reset_uri: str = Field(env="PASSWORD_RESET_URI", default="")
    django_rest_multitokenauth_reset_token_expiry_time: float = Field(
        env="DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME",
        default=1 / 6,  # 1/6 hour = 10 minutes
    )
    django_rest_passwordreset_timeout: int = Field(env="DJANGO_REST_PASSWORDRESET_TIMEOUT", default=60)
    django_rest_passwordreset_require_usable_password: bool = Field(
        env="DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD", default=False
    )

    # Cache config
    metrics_enabled: bool = Field(env="METRICS_ENABLED", default=True)
    redis_connection: str = Field(env="REDIS_CONNECTION", default="redis://redis:6379/0")

    # JWT token conf
    jwt_access_token_lifetime: int = Field(env="ACCESS_TOKEN_LIFETIME", default=60 * 30)  # 30 minutes
    jwt_refresh_token_lifetime: int = Field(env="REFRESH_TOKEN_LIFETIME", default=60 * 60 * 24)  # 24 hours


settings = ServiceSettings()
