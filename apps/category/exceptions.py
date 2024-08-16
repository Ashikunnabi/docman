from rest_framework import status

from apps.common.rest_utils.exceptions import BaseException


class GroupParentSameObjectException(BaseException):
    code = "GROUP_PARENT_AND_GROUP_CAN_NOT_BE_SAME"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Group parent can't be group itself"
