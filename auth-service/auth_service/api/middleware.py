from django_scopes import scope
from django_scopes import scopes_disabled
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CompanyScopingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to get authenticated user from request
        # At this point the request may contain Anonymous user even
        # though the user has authenticated. We have to fetch user
        # in order to be able to get the current company.
        with scopes_disabled():
            user = get_authenticated_user(request)

        if user.is_superuser:
            with scopes_disabled():
                return self.get_response(request)

        # TODO: change to company_scope context manager
        # Apply company scopes to the request
        company = getattr(user, "company", None)
        company_pk = company.pk if company else None
        with scope(company=company, company_pk=company_pk):
            return self.get_response(request)


def get_authenticated_user(request):
    """
    Attempts to return authenticated user from the request.
    If the request does not contain user or the user is not
    authenticated then an AnonymousUser will be returned.
    """
    try:
        result = JWTAuthentication().authenticate(request)
        if result is not None:
            return result[0]
    except Exception:
        pass

    return AnonymousUser()
