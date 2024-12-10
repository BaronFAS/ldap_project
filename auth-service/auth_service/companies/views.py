from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.serializers import CompanySerializer, CompanySerializerV2


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint Companies.
    """

    queryset = Company.objects.none()
    serializer_class = CompanySerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        return Company.objects.all()


class CompanyViewSet2(viewsets.ModelViewSet):
    serializer_class = CompanySerializerV2
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Company.objects.all().order_by("id")

        if user.is_authenticated:
            if not user.company:
                return Company.objects.none()
            return Company.objects.filter(id=user.company.id)
        return Company.objects.none()
