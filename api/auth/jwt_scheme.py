from typing import Tuple, Optional
from rest_framework import status, request, exceptions
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    AuthUser,
)
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(
        self, request: request.Request
    ) -> Optional[Tuple[AuthUser, AccessToken]]:
        header = self.get_header(request)
        if not header:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = AccessToken(raw_token, verify=False)
        except TokenError:
            raise exceptions.AuthenticationFailed(
                "Invalid token", code=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            validated_token.verify()
        except:
            return None
            
        user_id = validated_token.get(jwt_settings.USER_ID_CLAIM)
        if not user_id:
            raise exceptions.AuthenticationFailed(
                "Token contained no recognizable user identification",
                code=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            user = self.user_model.objects.get(**{jwt_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as e:
            raise exceptions.AuthenticationFailed(
                str(e), code=status.HTTP_401_UNAUTHORIZED
            )
        return (user, validated_token)

class CustomJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'api.auth.jwt_scheme.CustomJWTAuthentication' # Path to your custom class
    name = 'JWT Authentication' # Name to display in Swagger UI

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }