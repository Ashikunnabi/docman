from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.exceptions import InvalidCredentialsException
from apps.rbac.api.v1.serializers import UserInputSerializer
from apps.email.api.v1.viewsets import (
    new_user_notify_email_to_owner,
    recover_password_email,
)

from .serializers import LoginInputSerializer


@api_view(["POST"])
def login(request):
    data = request.data

    serializer = LoginInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    users = get_user_model().objects.filter(username=data.get("username"))

    if not users.exists():
        raise InvalidCredentialsException

    # activating session based authentication
    user = authenticate(
        username=request.data["username"], password=request.data["password"]
    )

    if not user:
        raise InvalidCredentialsException

    auth_login(request, user)
    token = {
        "user_id": user.uuid,
        "refresh": str(RefreshToken.for_user(users.first())),
        "access": str(RefreshToken.for_user(users.first()).access_token),
    }
    print(token)
    return Response(token, status=200)


@api_view(["POST"])
def registration(request):
    data = request.data
    files = request.FILES

    # store files in server
    for file in files:
        file_path = f"{settings.USER_INFORMATION_FILE_LOCATION}{files[file].name}"
        path = default_storage.save(file_path, files[file])
        data[file] = path

    # validating data
    serializer = UserInputSerializer(data=data)
    if not serializer.is_valid():
        return Response({"details": serializer.errors}, status=422)

    # given information is correct
    user_info = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password"),
        "phone": data.get("phone"),
        "company_name": data.get("company_name"),
        "company_email": data.get("company_email"),
        "company_address": data.get("company_address"),
        "company_employee_count": data.get("company_employee_count"),
        "company_application_document": data.get("company_application_document"),
        "company_store_front": data.get("company_store_front"),
        "company_commercial_location": data.get("company_commercial_location"),
        "company_reseller_permit": data.get("company_reseller_permit"),
        "company_retail_sales_floor": data.get("company_retail_sales_floor"),
    }

    user = get_user_model().objects.create_user(**user_info)
    new_user_notify_email_to_owner(request, user)

    return Response({"details": ["registration successful"]}, status=200)


@api_view(["POST"])
def recover_password(request):
    email = request.data.get("email", None)
    if not email:
        return Response({"details": "Email address not found"})

    users = get_user_model().objects.filter(email=email)

    if not users.exists():
        return Response({"details": "Email address not found"})

    data = {
        "uuid": str(users.first().uuid),
        "email": str(users.first().email),
    }
    recover_password_email(request, data)

    return Response({"details": ["Mail send successful"]}, status=200)


@api_view(["POST"])
def recover_password_now(request):
    data = request.data
    uuid = data.get("uuid", None)
    password = data.get("password", None)

    if not uuid:
        return Response({"details": "Something went wrong"})
    if not password:
        return Response({"details": "Enter new password went wrong"})

    users = get_user_model().objects.filter(uuid=uuid)

    if not users.exists():
        return Response({"details": "Details not found"})

    users.first().set_password(password)
    users.first().save()
    return Response(
        {"details": ["Password recovered successfully. Please login to continue"]},
        status=200,
    )
