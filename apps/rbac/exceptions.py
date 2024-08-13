from rest_framework import status

from apps.common.exceptions import BaseException


class UserDeletionNotAllowedException(BaseException):
    code = "USER_DELETION_NOT_ALLOWED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User deletion not allowed"
