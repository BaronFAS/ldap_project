from typing import Union

from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import set_rollback
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        detail = exctract_error(exc.detail)

        data = {
            "detail": detail,
        }

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


def exctract_error(error: Union[str, list, ErrorDetail, dict[str, Union[str, list, ErrorDetail]]]) -> str:
    if isinstance(error, dict):
        errors = []
        for field, err in error.items():
            err = exctract_error(err)
            if field == "non_field_errors":
                errors.append(f"{err}")
            else:
                errors.append(f"Field: {field}. Error: {err}")
        detail = "\n".join(errors)
    elif isinstance(error, (list, tuple)):
        detail = "\n".join([exctract_error(err) for err in error])
    else:
        detail = str(error)

    return detail
