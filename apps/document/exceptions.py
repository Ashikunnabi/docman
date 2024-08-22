from rest_framework import status

from apps.common.exceptions import BaseException


class FileRequiredException(BaseException):
    code = "FILE_REQUIRED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "File is required"


class FileSizeExceededException(BaseException):
    code = "FILE_SIZE_EXCEEDED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "File size exceeded"


class FileExtensionNotAllowedException(BaseException):
    code = "FILE_EXTENSION_NOT_ALLOWED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "File extension not allowed"

class CategoryNotAccessableException(BaseException):
    code = "CATEGORY_NOT_ACCESSABLE"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Category not accessable"
