from contextlib import contextmanager
from unittest import mock


@contextmanager
def authenticated_user(user):
    with mock.patch("api.middleware.JWTAuthentication.authenticate") as authenticate:
        authenticate.return_value = user, None
        yield user
