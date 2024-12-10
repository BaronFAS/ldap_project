from contextlib import contextmanager

from django_scopes import scope
from django_scopes import scopes_disabled


@contextmanager
def company_scope(user):
    """Apply user's company scope"""
    if user.is_superuser:
        with scopes_disabled():
            yield
    else:
        company = getattr(user, "company", None)
        company_pk = company.pk if company else None
        with scope(company=company, company_pk=company_pk):
            yield
