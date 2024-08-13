from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.core import signing
from django.shortcuts import redirect, render


def login(request):
    # after login redirect to next url otherwise default login redirect url
    _next = request.GET.get("next", settings.LOGIN_REDIRECT_URL)

    if not request.user.is_authenticated:
        return render(request, "authentication/login.html")
    return redirect(_next)


def registration(request):
    if not request.user.is_authenticated:
        return render(request, "authentication/account.html")
    return redirect(settings.LOGIN_REDIRECT_URL)


def logout(request):
    auth_logout(request)
    return redirect(settings.LOGIN_URL)


def account_activation(request):
    rt = request.GET.get("rt")
    au = request.GET.get("au")
    context = {"rt": rt, "au": au}
    return render(request, "authentication/account_activation.html", context)


def recover_password(request):
    return render(request, "authentication/recover_password.html")


def recover_password_now(request, hash_id):
    try:
        val = signing.loads(hash_id)
    except Exception as ex:
        return redirect(settings.LOGIN_URL)
    return render(
        request, "authentication/recover_password_now.html", context={"data": val}
    )
