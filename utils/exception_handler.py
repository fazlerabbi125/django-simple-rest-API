from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import exception_handler
from .common import failure_response
from django.core.exceptions import ValidationError


def custom_exception_handler(exc: Exception, context: dict = {}):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # print(context)
    
    err_res = exception_handler(exc, context)
    if err_res is None:
        return err_res

    if isinstance(exc, (ValidationError, serializers.ValidationError)):
        return Response(
            failure_response(
                errors=err_res.data,
                message="The given data was invalid",
            ),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(failure_response(message=str(exc)), status=err_res.status_code)
