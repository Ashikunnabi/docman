from rest_framework import status

from apps.common.rest_utils.exceptions import BaseException


class GroupParentSameObjectException(BaseException):
    code = "GROUP_PARENT_AND_GROUP_CAN_NOT_BE_SAME"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Group parent can't be group itself"


class InvalidCategoryPermissionTypeException(BaseException):
    code = "INVALID_CATEGORY_PERMISSION_TYPE"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Invalid category permission type"


class UserNotSetException(BaseException):
    code = "USER_NOT_SET"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User is not set"
