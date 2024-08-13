from __future__ import unicode_literals

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    MethodNotAllowed,
    NotFound,
    ValidationError,
)
from rest_framework.response import Response
from six import string_types


class BaseException(Exception):
    """
    Internal exception base class that can be handled by the exception handler.
    """

    code = None
    errors = None
    message = ""
    identifier = None
    context = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message="",
        context=None,
        errors=None,
        identifier=None,
        code=None,
        *args,
        **kwargs
    ):
        self.code = code or self.code
        self.message = message or self.message
        self.errors = errors or self.errors
        self.context = context or self.context
        self.identifier = identifier or self.identifier

        if kwargs:
            self.context.update(kwargs)

        if self.context and self.message:
            self.message = self.message.format(**self.context)

    def __str__(self):
        return str(self.message)


class BadRequestException(BaseException):
    code = "BAD_REQUEST"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Invalid input"


class InvalidInputException(BadRequestException):
    code = "INVALID_INPUT"


def exception_handler(exc, context=None):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException` and Django's builtin
    `Http404` exceptions.

    Any unhandled exceptions are catched and logged by this handler and
    an `OperationException` is raised accordingly the view or process behind
    that triggered the actual error.
    """

    if isinstance(exc, Http404):
        exc = NotFound()
    elif isinstance(exc, ValidationError):
        exc = InvalidInputException(errors=exc.detail)

    # Make sure were always working with an APIException or BaseException
    if not isinstance(exc, (APIException, BaseException)):
        raise exc

    identifier = getattr(exc, "identifier", None)
    code = getattr(exc, "code", "")
    message = getattr(exc, "message", "")
    errors = getattr(exc, "errors", [])

    if not code and isinstance(exc, APIException):
        # DRF 3.5 exceptions have a proper code we can expose
        if hasattr(exc, "get_codes"):
            codes = exc.get_codes()
            if isinstance(codes, string_types):
                code = codes
            else:
                code = next(iter(codes))

        # Fallback to the default OPERATION_FAILED message
        # if also no default_code was provided
        code = code or getattr(exc, "default_code", "OPERATION_FAILED")
        code = code.upper()

    if isinstance(exc, MethodNotAllowed):
        code = "NOT_ALLOWED"
    elif isinstance(exc, NotFound):
        code = "NOT_FOUND"

    data = dict(message=message, errors=errors, key=identifier, code=code)

    return Response(data, status=exc.status_code)
