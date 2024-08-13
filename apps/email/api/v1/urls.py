from django.urls import include, path

from .viewsets import *


app_name = 'v1'


urlpatterns = [
    path(
        'send-account-activation-email/',
        send_account_activation_email_to_user,
        name='send_account_activation_email_to_user'
    ),
]
