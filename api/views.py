from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from utils.common import success_response, failure_response


@api_view(["GET", "POST"])
def get_author_list_or_create(request: HttpRequest):
    match request.method:
        case "GET":
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(
                success_response(
                    data=serializer.data,
                    message="Authors successfully fetched.",
                ),
                status=status.HTTP_200_OK,
            )
        case "POST":
            serializer = AuthorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    failure_response(
                        errors=serializer.errors,
                        message="Given data is invalid for author",
                    ),
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            serializer.save()
            return Response(
                success_response(
                    data=serializer.data,
                    message="Author successfully created.",
                ),
                status=status.HTTP_201_CREATED,
            )
