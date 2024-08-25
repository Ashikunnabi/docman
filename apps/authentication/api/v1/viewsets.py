from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import (
    BlacklistedToken,
    OutstandingToken,
    RefreshToken,
)

from apps.email.api.v1.viewsets import (
    new_user_notify_email_to_owner,
    recover_password_email,
)
from apps.rbac.api.v1.serializers import UserInputSerializer

from ...exceptions import InvalidCredentialsException
from .serializers import LoggedInUserOutputSerializer, LoginInputSerializer


@api_view(["POST"])
@permission_classes([])
def login(request):
    # Deserialize input data
    serializer = LoginInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    password = serializer.validated_data.get("password")

    # activating session based authentication
    user = authenticate(username=username, password=password)

    if not user:
        raise InvalidCredentialsException

    auth_login(request, user)

    # Generate JWT tokens
    try:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    except InvalidToken as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    token = {
        "user": LoggedInUserOutputSerializer(user).data,
        "refresh": str(refresh),
        "access": str(access),
    }
    return Response(token, status=200)


@api_view(["POST"])
def logout(request):
    """
    Logout the user by blacklisting the JWT token.
    """
    if request.user and request.auth:
        try:
            # Blacklist the token
            outstanding_token = OutstandingToken.objects.get(
                token=request.data["refresh"]
            )
            BlacklistedToken.objects.create(token=outstanding_token)
            outstanding_token.delete()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except OutstandingToken.DoesNotExist:
            return Response(
                {"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"detail": "User not authenticated."}, status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["POST"])
@permission_classes([])
def refresh_token(request):
    """
    Refresh the JWT token.
    """
    try:
        refresh = RefreshToken(request.data["refresh"])
        access = refresh.access_token
    except InvalidToken as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    token = {
        "refresh": str(refresh),
        "access": str(access),
    }
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
@permission_classes([])
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
@permission_classes([])
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
