from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .viewsets import login, recover_password, recover_password_now, registration

app_name = "v1"

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", login, name="login"),
    path("registration/", registration, name="registration"),
    path("recover-password/", recover_password, name="recover_password"),
    path("recover-password-now/", recover_password_now, name="recover_password_now"),
]
