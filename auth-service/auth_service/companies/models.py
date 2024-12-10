import uuid

from django.db import models
# from django_scopes import ScopedManager

from safedelete.models import SafeDeleteModel, SOFT_DELETE


class Company(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    short_name = models.CharField(max_length=512)
    domain_url = models.URLField(max_length=512, default="")
    password_reset_uri = models.URLField(max_length=512, default="")

    # objects = ScopedManager(company_pk="pk")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "company"
        verbose_name = "company"
        verbose_name_plural = "Companies"
