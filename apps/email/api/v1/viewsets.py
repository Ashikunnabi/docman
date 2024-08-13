from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.files.storage import default_storage

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.utils.basic import *
from apps.common.utils.send_email import SendEmail


@api_view(http_method_names=['POST'])
def send_account_activation_email_to_user(request):
    data = request.data

    # request.data must contain user's uuid. {'id': uuid}
    if 'id' not in data.keys():
        return Response({"data": "User id not found"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    users = get_user_model().objects.filter(uuid=data['id'])

    # if no user found with given uuid
    if not users.exists():
        return Response({"data": "User id not found"}, status=status.HTTP_404_NOT_FOUND)

    # collect first user
    user = users.first()

    # if user is no active only then account activation email will be send
    if user.is_active:
        return Response({"data": "User is already active."}, status=status.HTTP_403_FORBIDDEN)

    # collect user's email address
    email_address_of_selected_user = user.email

    # generate JWT refresh token to send as activation url
    refresh_token = RefreshToken.for_user(user)

    # The HTTP Host header sent by the client
    activation_url = request.build_absolute_uri(
        f'/account/activation/?rt={str(refresh_token)}&au={user.activation_url}'
    )

    # send activation email
    subject = 'Active your account'
    body = 'Please click the link to active your account'
    email_address = [email_address_of_selected_user]
    html_template_path = 'send_email/account_activation/account_activation_email_template.html'
    context = {
        'host_url': f'{request.build_absolute_uri("/")[:-1]}',
        'activation_url': f'{activation_url}',
        'company_email': settings.COMPANY_EMAIL,
        'company_phone': settings.COMPANY_PHONE
    }

    send_email = SendEmail(
        subject=subject,
        body=body,
        to=email_address
    ).html_email(html_template_path=html_template_path, context=context)

    # failed to send
    if 'Mail send successfully' not in send_email:
        return Response({"data": send_email}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"data": send_email})


def new_user_notify_email_to_owner(request, data):
    subject = 'A New User Registered'
    body = f'There is a new user waiting for approval. ' \
        f'{data.name} ({data.email}, {data.phone}). ' \
        f'\nLink: {request.build_absolute_uri("/admin/user")}/edit/{data.uuid}'
    email_address = [settings.EMAIL_HOST_USER]

    SendEmail(
        subject=subject,
        body=body,
        to=email_address
    ).simple_email()


def new_order_notify_email_to_owner(request, data):
    subject = 'A New Order Placed'
    body = f'There is a new order by ' \
        f'{data.user.name} ({data.user.email}, {data.user.phone}). ' \
        f'\nOrder ID: 140{data.id} ' \
        f'\nLink: {request.build_absolute_uri("/admin/order")}/edit/{data.uuid}'
    email_address = [settings.EMAIL_HOST_USER]

    SendEmail(
        subject=subject,
        body=body,
        to=email_address
    ).email_with_attachment(default_storage.path(data.invoice))


def recover_password_email(request, data):
    subject = 'Recover Password'
    body = f'To recover your password please go to the given link\n' \
        f'{request.build_absolute_uri("/recover-password/"+signing.dumps(data))}'
    email_address = [data['email']]

    SendEmail(
        subject=subject,
        body=body,
        to=email_address
    ).simple_email()
