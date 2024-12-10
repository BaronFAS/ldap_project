import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    Group, BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.management.utils import get_random_secret_key
from safedelete.models import SafeDeleteModel, SOFT_DELETE
from safedelete.managers import SafeDeleteManager

from companies.models import Company


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager, SafeDeleteManager):

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(
        self,
        email,
        password=None,
        first_name=None,
        last_name=None,
        staff=False,
        admin=False,
        company=None,
        roles=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email).lower(),
            first_name=first_name,
            last_name=last_name,
            staff=staff,
            admin=admin,
            company=company,
        )

        user.set_password(password)
        user.save(using=self._db)

        if roles is not None:
            user.role.set([roles])

        return user

    def create_staff_user(
        self,
        email,
        password,
        first_name=None,
        last_name=None
    ):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password,
        first_name=None,
        last_name=None
    ):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.staff = True
        user.admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Role(Group):
    class Meta:
        proxy = True
        db_table = "role"
        verbose_name = "role"
        verbose_name_plural = "roles"


class Statuses(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "deactivated"


class User(
    AbstractBaseUser, PermissionsMixin, SafeDeleteModel, TimestampMixin
):
    _safedelete_policy = SOFT_DELETE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email address",
        max_length=512,
        unique=True,
        db_index=True,
    )
    secret_key = models.CharField(
        max_length=255,
        default=get_random_secret_key
    )
    first_name = models.CharField(
        verbose_name="first name",
        max_length=25,
        default="",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=25,
        default="",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        default=None,
        blank=True,
        null=True,
        max_length=128
    )

    role = models.ManyToManyField(
        Role,
        through="RoleUser",
        related_name="users")

    is_active = models.BooleanField(default=True)
    # Staff can login into Django Admin
    staff = models.BooleanField(default=False)
    # Deprecated in favor of Admin role
    admin = models.BooleanField(default=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
    )
    last_password_reset = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined",
        default=timezone.now
    )

    # objects = ScopedManager(company="company", _manager_class=UserManager)
    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

        permissions = (
            ("view_user_id", "Can view user id"),
            ("view_user_is_active", "Can view user status"),
            ("change_user_data", "Can change user data"),
            ("change_their_avatar", "Can change their avatar"),
        )

    USERNAME_FIELD = "email"
    # email & password are required by default.
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """
        Staff user is a Super Admin and can manage objects from all companies.
        """
        return self.staff

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
        if self.role.exists():
            self.groups.set(self.role.all())


class RoleUser(models.Model):
    role = models.ForeignKey(
        Role,
        models.SET_NULL,
        default=None,
        null=True
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        default=None,
        null=True
    )

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.Role} {self.User}"
