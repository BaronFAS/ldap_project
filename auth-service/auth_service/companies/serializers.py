from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = "__all__"


class CompanySerializerV2(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "short_name",
            "domain_url",
            "password_reset_uri"
        )
