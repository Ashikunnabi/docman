from rest_framework import status

from apps.common.exceptions import BaseException


class UserDeletionNotAllowedException(BaseException):
    code = "USER_DELETION_NOT_ALLOWED"
    message = "User deletion not allowed"
    status_code = status.HTTP_400_BAD_REQUEST


class UserCurrentPasswordIncorrectException(BaseException):
    code = "USER_CURRENT_PASSWORD_INCORRECT"
    message = "Current password is incorrect"
    status_code = status.HTTP_400_BAD_REQUEST


class UserNewPasswordNotMatchedException(BaseException):
    code = "USER_NEW_PASSWORD_NOT_MATCHED"
    message = "New password and confirm password not matched"
    status_code = status.HTTP_400_BAD_REQUEST
