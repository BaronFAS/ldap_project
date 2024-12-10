from rest_framework.views import APIView
# from rest_framework.request import Request
from rest_framework.generics import get_object_or_404
# from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# from auth.services import gen_cloud_core_auth_key


class NestedViewMixin:
    nested_lookup = None
    nested_parent_class = None

    def get_nested_parent_object(self):
        return get_object_or_404(self.nested_parent_class, pk=self.kwargs[f"{self.nested_lookup}_pk"])

    def get_nested_filter(self):
        return {
            self.nested_lookup: self.get_nested_parent_object(),
        }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(**self.get_nested_filter())

        return queryset


class JWTGenerateView(APIView):
    authentication_classes = [
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    # def get(self, request: Request) -> Response:
    #     access_token = gen_cloud_core_auth_key()
    #     return Response(
    #         data={"access_token": access_token},
    #         status=200,
    #     )
