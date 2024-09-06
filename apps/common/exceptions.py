from rest_framework import status

from .rest_utils.exceptions import BaseException


class ServiceClassNotFoundException(BaseException):
    code = "SERVICE_CLASS_NOT_FOUND"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Service class not found"


class InputSerializerNotFoundException(BaseException):
    code = "INPUT_SERIALIZER_NOT_FOUND"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Input serializer not found"


class OutputSerializerNotFoundException(BaseException):
    code = "OUTPUT_SERIALIZER_NOT_FOUND"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Output serializer not found"


class ObjectAlreadyExistsException(BaseException):
    code = "OBJECT_ALREADY_EXISTS"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Object already exists"

class ObjectNotFoundException(BaseException):
    code = "OBJECT_NOT_FOUND"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Object not found"

class LimitExceededException(BaseException):
    code = "LIMIT_EXCEEDED"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Limit exceeded. Can't add more. Please contact support for more information."
