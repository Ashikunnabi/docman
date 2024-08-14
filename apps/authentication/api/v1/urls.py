from django.urls import path

from .viewsets import (
    login,
    logout,
    recover_password,
    recover_password_now,
    registration,
)


app_name = "v1"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("registration/", registration, name="registration"),
    path("recover-password/", recover_password, name="recover_password"),
    path("recover-password-now/", recover_password_now, name="recover_password_now"),
]
