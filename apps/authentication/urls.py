from django.urls import include, path

from .views import (
    account_activation,
    login,
    logout,
    recover_password,
    recover_password_now,
    registration,
)

app_name = "authentication"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("registration/", registration, name="registration"),
    path("account/activation/", account_activation, name="account_activation"),
    path("recover-password/", recover_password, name="recover_password"),
    path(
        "recover-password/<str:hash_id>/",
        recover_password_now,
        name="recover_password_now",
    ),
    path("api/", include("apps.authentication.api.urls")),
]
