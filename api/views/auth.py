from django.shortcuts import get_object_or_404
from rest_framework import status, request, exceptions, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import User
from ..serializers import LoginSerializer
from utils.common import success_response, failure_response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..auth import permissions as custom_permissions
from rest_framework_simplejwt.settings import api_settings as jwt_settings


@api_view(["POST"])
@permission_classes([custom_permissions.IsGuest])
def login(request: request.Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        request,
        email=serializer.data.get("email"),
        password=serializer.data.get("password"),
    )

    if not user:
        raise exceptions.AuthenticationFailed()

    refresh = RefreshToken.for_user(user)
    return Response(
        success_response(
            message="Login successful",
            data={
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            },
        )
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request: request.Request):
    try:
        refresh_token = request.data.get("refresh_token", "")
        # new token if first arg is None; otherwise decode and validate the encoded token given by the first arg
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            success_response(message="Logout successful"),
            status=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        return Response(
            failure_response(message=str(e)), status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def renew_tokens(request: request.Request):
    try:
        refresh_token = request.data.get("refresh_token")
        old_token = RefreshToken(refresh_token)
        user_id = old_token.payload.get(jwt_settings.USER_ID_CLAIM)
        old_token.blacklist()
        user = get_object_or_404(User, **{jwt_settings.USER_ID_FIELD: user_id})
        new_refresh_token = RefreshToken.for_user(user)

        return Response(
            success_response(
                message="Renewal successful",
                data={
                    "refresh_token": str(new_refresh_token),
                    "access_token": str(new_refresh_token.access_token),
                },
            ),
        )
    except Exception as e:
        return Response(
            failure_response(message=str(e)), status=status.HTTP_400_BAD_REQUEST
        )
