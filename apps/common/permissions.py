from rest_framework import permissions
from apps.common.rest_utils.exceptions import BadRequestException


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    This permission layer will fetch the services from the APIview
    Based on the services we must know the 'main' model
    API access is determined based on the CRUD of the model
    Special access is handled within the service if required
    For this, you must make sure you add extra permissions to the model itself
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def _model_from_services(self, view):
        """
        This will return the available (base) model on the service
        :param view:
        :return:
        """
        assert getattr(view, 'service_class', None) is not None, (
            'Cannot apply {} on view {} that does not set '
            '`.service_class`'
        ).format(self.__class__.__name__, view)

        if not view.service_class.model:
            raise BadRequestException(
                errors=f"Miss-configured service added in the API. Value for attribute 'model' is missing in service.",
                message=f"Miss-configured service added in the API. Value for attribute 'model' is missing in service."
            )

        return view.service_class.model.objects.none()

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._model_from_services(view)
        perms = self.get_required_permissions(request.method, queryset.model)

        return request.user.has_perms(perms)


class IsDashboardUser(permissions.BasePermission):
    """
    Allows access only to authenticated dashboard users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_anonymous and request.user.is_dashboard)


class IsAnonymousAllowed(permissions.BasePermission):
    """
    if the site allows anonymous user returns true else false
    """
    message = 'Site does not allow anonymous user. Please login.'

    def has_permission(self, request, view):
        is_permitted = False
        if request.site_profile.allow_anonymous_registration:
            is_permitted = True
        return is_permitted


class IsAnonymousAllowedOrAuthorized:
    """
    If an anonymous user is allowed, then allow request.
    Otherwise, check regular permissions.
    """
    def check_permissions(self, request):
        anonymous_allowed = IsAnonymousAllowed().has_permission(request, self)
        if not anonymous_allowed:
            super().check_permissions(request)
