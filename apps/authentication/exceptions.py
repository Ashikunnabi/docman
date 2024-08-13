from rest_framework import status

from apps.common.rest_utils.exceptions import BaseException


class InvalidCredentialsException(BaseException):
    code = "INVALID_CREDENTIALS"
    message = "Invalid credentials"
    status_code = status.HTTP_400_BAD_REQUEST
