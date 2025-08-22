from rest_framework import status, request, exceptions, serializers, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..serializers import LoginSerializer, UserSerializer
from utils.common import success_response, failure_response, SwaggerTags
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# , TokenBlacklistSerializer, TokenObtainPairSerializer


@extend_schema(
    summary="User Login",
    description="Authenticates a user.",
    request=LoginSerializer,
    tags=[SwaggerTags.AUTH.value],
)
@api_view(["POST"])
@permission_classes([~permissions.IsAuthenticated]) # & (and), | (or) and ~ (not)
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
                "user": UserSerializer(user).data,
            },
        )
    )


SwaggerRefreshTokenRequest = inline_serializer(
    name="RefreshTokenRequest",
    fields={
        "refresh_token": serializers.CharField(),
    },
)

# {
#     "type": "object",
#     "properties": {
#         "refresh_token": {"type": "string", "example": "eyJhbGciOi..."},
#     },
# }


@extend_schema(
    summary="User Logout",
    description="Logs out a user.",
    request=SwaggerRefreshTokenRequest,
    tags=[SwaggerTags.AUTH.value],
)
@api_view(["POST"])
def logout(request: request.Request):
    refresh_token = request.data.get("refresh_token", "")
    if not refresh_token:
        raise exceptions.APIException(
            "Refresh token is required", status.HTTP_400_BAD_REQUEST
        )
    try:
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


@extend_schema(
    summary="Renew Tokens",
    description="Renews access and refresh tokens.",
    request=SwaggerRefreshTokenRequest,
    tags=[SwaggerTags.AUTH.value],
)
@api_view(["POST"])
def renew_tokens(request: request.Request):
    serializer = TokenRefreshSerializer(
        data={"refresh": request.data.get("refresh_token", "")}
    )
    serializer.is_valid(raise_exception=True)
    # if not refresh_token:
    #     raise exceptions.APIException(
    #         "Refresh token is required", status.HTTP_400_BAD_REQUEST
    #     )
    # try:
    #     old_token = RefreshToken(refresh_token)
    #     user_id = old_token.payload.get(jwt_settings.USER_ID_CLAIM)
    #     old_token.blacklist()
    #     user = get_object_or_404(User, **{jwt_settings.USER_ID_FIELD: user_id})
    #     new_refresh_token = RefreshToken.for_user(user)

    return Response(
        success_response(
            message="Renewal successful",
            data={
                "refresh_token": serializer.data["refresh"],
                "access_token": serializer.data["access"],
            },
        ),
    )
    # except Exception as e:
    #     return Response(
    #         failure_response(message=str(e)), status=status.HTTP_400_BAD_REQUEST
    #     )
