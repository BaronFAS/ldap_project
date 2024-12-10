import logging

from rest_framework import serializers
from rest_framework.fields import empty
from django.core.exceptions import PermissionDenied
from django.core.validators import EmailValidator, RegexValidator
# from companies.models import DashboardLinks
# from assets.serializers import AssetSerializer
# from companies.serializers import DashboardLinksSerializer
# from django_rest_passwordreset.models import ResetPasswordToken
# from django_rest_passwordreset.email_sender import password_reset_token_created
# from django_rest_passwordreset.signals import reset_password_token_created

from accounts.models import Role, User, Statuses
from accounts.validators import PhoneNumberValidator
from companies.models import Company
from auth_service.config import PHONE_VALIDATE
from accounts.utils import LDAPManager


logging.basicConfig(level=logging.INFO)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
        default=None,
    )
    status = serializers.SerializerMethodField()
    # image = AssetSerializer(required=False, allow_null=True)
    # dashboard_links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "status",
            "is_active",
            "company_id",
            "company_name",
            # "image",
            # "dashboard_links",
        ]

    def get_id(self, obj):
        user = self.context["request"].user
        if user == obj or user.has_perm("accounts.view_user_id"):
            return obj.id
        return None

    def get_is_active(self, obj):
        user = self.context["request"].user
        if user == obj or user.has_perm("accounts.view_user_is_active"):
            return obj.is_active
        return None

    def get_status(self, obj):
        return Statuses.ACTIVE if obj.is_active else Statuses.INACTIVE

    # def get_dashboard_links(self, obj):
    #     resp = []
    #     company_id = obj.company_id
    #     dashboard_links = DashboardLinks.objects.filter(
    #         company_id=company_id
    #     )
    #     for dashboard_link in dashboard_links:
    #         serializer = DashboardLinksSerializer(dashboard_link)
    #         resp.append(serializer.data)
    #     return resp

    def create(self, validated_data):
        # image = validated_data.pop("image", empty)
        user = super().create(validated_data)
        # if image is not empty:
        #     user.image = image
        user.company = self.context["request"].user.company
        if user.role is None:
            user.role, _ = Role.objects.get_or_create(name="Mission Operator")
        user.save()

        # token = ResetPasswordToken.objects.create(
        #     user=user,
        # )
        # password_reset_token_created(token, invite=True) TODO раскомментировать когда настроим свой почтовый сервер
        user.save()
        return user

    def update(self, instance, validated_data):
        u = self.context["request"].user

        if not validated_data:
            validated_data = self.context["request"].data

        if not u.has_perm("accounts.change_user_data"):
            if u != instance or validated_data.keys() - {"image"} or not u.has_perm("accounts.change_their_avatar"):
                raise PermissionDenied
        image = validated_data.pop("image", empty)
        if image is not empty:
            instance.image = image

        is_active = self.context["request"].data.get("status", empty)
        if is_active is not empty:
            if is_active == Statuses.ACTIVE:
                validated_data["is_active"] = True
            elif is_active == Statuses.INACTIVE:
                validated_data["is_active"] = False
            else:
                variants = [Statuses.ACTIVE, Statuses.INACTIVE]
                raise serializers.ValidationError({
                    "status": f"The Status field is not valid. The allowed values are {', '.join(variants)}",
                })

        return super().update(instance=instance, validated_data=validated_data)


class UserSerializerV2(serializers.ModelSerializer):
    """Serializer that receives a user and a list of users."""

    role = RoleSerializer(required=False, many=True)
    company_id = serializers.UUIDField(
        source="company.id",
        read_only=True
    )
    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.company:
            data['company_id'] = None
            data['company_name'] = None
        return data

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "is_active",
            "company_id",
            "company_name",
        ]


class UserPostUpdateSerializerV2(UserSerializerV2):
    """Serializer that creates and updates the user."""

    role_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    company_id = serializers.UUIDField(write_only=True)
    email = serializers.EmailField(validators=[EmailValidator()])

    forbidden_characters_validator = RegexValidator(
        r'^[^!@#$%^&*()+=\[\]{};:<>,.?/\\ ]+$',
        'The field contains forbidden characters.'
    )
    first_name = serializers.CharField(
        validators=[forbidden_characters_validator]
    )
    last_name = serializers.CharField(
        validators=[forbidden_characters_validator]
    )
    if not PHONE_VALIDATE:
        phone_number = serializers.CharField(
            validators=[PhoneNumberValidator()]
        )

    def create(self, validated_data):
        roles_ids = validated_data.pop('role_ids', [])
        company_id = validated_data.pop('company_id')
        user = User.objects.create(**validated_data)

        for role_id in roles_ids:
            role = Role.objects.get(id=role_id)
            user.role.add(role)

        if company_id:
            company = Company.objects.get(id=company_id)
            user.company = company
            user.save()
        # Start adding user to LDAP
        with LDAPManager() as ldap_manager:
            user_data = ldap_manager.create_user_data(user)
            ldap_manager.add_new_user(user_data)
        # End adding user to LDAP
        return user

    def update(self, user, validated_data):
        roles_ids = validated_data.pop('role_ids', [])
        company_id = validated_data.pop('company_id', None)

        for attr, value in validated_data.items():
            setattr(user, attr, value)

        user.role.clear()
        for role_id in roles_ids:
            role = Role.objects.get(id=role_id)
            user.role.add(role)

        if company_id:
            company = Company.objects.get(id=company_id)
            user.company = company

        user.save()
        # Start change user to LDAP
        with LDAPManager() as ldap_manager:
            user_data = ldap_manager.create_user_data(user)
            ldap_manager.add_new_user(user_data)
        # End change user to LDAP
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        role_names = instance.role.all().values_list('name', flat=True)
        data['role'] = list(role_names) if role_names else []
        if instance.company:
            data['company_name'] = instance.company.name
        else:
            data['company_name'] = None
        return data

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role_ids",
            "is_active",
            "company_id",
        ]


class RoleSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")
