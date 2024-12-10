from rest_framework import serializers

from accounts.models import Role, User
from companies.models import Company


class RoleSerializerExternal(serializers.ModelSerializer):
    """Serializer to get roles."""
    class Meta:
        model = Role
        fields = ("id", "name")


class UserSerializerExternal(serializers.ModelSerializer):
    """Serializer to get user."""

    role = RoleSerializerExternal(required=False, many=True)
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


class CompanySerializerExternal(serializers.ModelSerializer):
    """Serializer to get company."""
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "short_name",
            "domain_url",
            "password_reset_uri"
        )
