from rest_framework.request import Request, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from utils.common import success_response, failure_response


@api_view(["GET", "POST"])
def authorList(request: HttpRequest | Request):
    match request.method:
        case "GET":
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(
                success_response(
                    data=serializer.data,
                    message="Authors successfully fetched.",
                ),
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


class AuthorDetails(APIView):
    def _get_object(self, pk: int):
        return Author.objects.get(pk=pk)

    def get(self, request: HttpRequest | Request, authorId: int):
        author = self._get_object(authorId)
        serializer = AuthorSerializer(author)
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully fetched.",
            ),
        )

    def put(self, request: HttpRequest | Request, authorId: int):
        # Complete update (as partial arg in serializer not provided or is false). Throws exception if all necessary fields are not present
        author = self._get_object(authorId)
        serializer = AuthorSerializer(instance=author, data=request.data)
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
                message="Author successfully updated via PUT method.",
            ),
        )

    def patch(self, request: HttpRequest | Request, authorId: int):
        # Partial update (via partial=True). Fields which are not provided are not updated.
        author = self._get_object(authorId)
        serializer = AuthorSerializer(instance=author, data=request.data, partial=True)
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
                message="Author successfully updated via PATCH method.",
            ),
        )

    def delete(self, request: HttpRequest | Request, authorId: int):
        author = self._get_object(authorId)
        author.delete()
        return Response(
            success_response(message="Author successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )

    def handle_exception(self, exc):
        # Overriding parent exeception handler

        if isinstance(exc, (Author.DoesNotExist)):
            return Response(
                failure_response(
                    message="Author not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().handle_exception(exc)
