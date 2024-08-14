from rest_framework import status

from apps.common.exceptions import BaseException


class FileRequiredException(BaseException):
    code = "FILE_REQUIRED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "File is required"
