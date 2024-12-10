from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Services(TimestampMixin, models.Model):
    """Model for storing data about a custom
    jwt token for API external services."""
    service_name = models.CharField(
        verbose_name="Service name",
        max_length=128,
        default=None,
        blank=True,
        null=True,
    )
    jwt_token = models.CharField(
        verbose_name="JWT token",
        max_length=500,
        default=None,
        blank=True,
        null=True,
    )
    service_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.service_name}"
