from django.shortcuts import get_object_or_404
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import User
from ..serializers import LoginSerializer
from utils.common import success_response, failure_response
from django.contrib.auth import authenticate


@api_view(["POST"])
def login(request: request.Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = authenticate(
        request,
        email=serializer.data.get("email"),
        password=serializer.data.get("password"),
    )
    

    if not user:
        return Response(
            failure_response("Invalid user"), status=status.HTTP_401_UNAUTHORIZED
        )

    return Response(
        success_response(message="Login successful"), status=status.HTTP_204_NO_CONTENT
    )
