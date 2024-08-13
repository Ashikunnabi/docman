from re import compile

from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from apps.rbac import models

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/"))]

if hasattr(settings, "LOGIN_EXEMPT_URLS"):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    """Checking User authentication before serving response"""

    def process_request(self, request):
        path = request.path_info.lstrip("/")
        if request.user.is_anonymous:
            # if not any(m.match(path) for m in EXEMPT_URLS):
            if path.startswith("admin"):
                return redirect(settings.LOGIN_URL + "?next=/" + path)
        else:
            if not request.user.is_active:
                logout(request)
                if not any(m.match(path) for m in EXEMPT_URLS):
                    return redirect(settings.LOGIN_URL)
            if request.user.is_staff:
                if (
                    not path.startswith("admin")
                    and not any(m.match(path) for m in EXEMPT_URLS)
                    and not path.startswith("logout")
                    and not path.startswith("media")
                ):
                    return redirect("/admin/" + path)
            if not request.user.is_staff and path.startswith("admin"):
                return redirect("/")


def RequestExposerMiddleware(get_response):
    """Pass request object to rbac.models"""

    def middleware(request):
        models.exposed_request = request
        response = get_response(request)
        return response

    return middleware
