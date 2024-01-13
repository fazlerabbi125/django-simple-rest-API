from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Author
from ..serializers import AuthorSerializer
from utils.common import success_response, failure_response


@api_view(["GET", "POST"])
def authorList(request):
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
                        message="Given data is invalid for Author",
                    ),
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            serializer.save()
            # To get only the validated incoming data (consists only the fields passed), use serializer.validated_data
            return Response(
                success_response(
                    data=serializer.data,
                    message="Author successfully created.",
                ),
                status=status.HTTP_201_CREATED,
            )


class AuthorDetail(APIView):
    def _get_object(self, pk: int):
        return get_object_or_404(Author, pk=pk) #first arg can be either Model, Manager, or QuerySet object

    def _get_serializer(self, *args, **kwargs):
        return AuthorSerializer(*args, **kwargs)

    def get(self, request, authorId: int):
        author = self._get_object(authorId)
        serializer = self._get_serializer(author)
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully fetched.",
            ),
        )

    def put(self, request, authorId: int):
        # Complete update (as partial arg in serializer is not provided or false here). Throws exception if all necessary fields are not present
        author = self._get_object(authorId)
        serializer = self._get_serializer(instance=author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully updated via PUT method.",
            ),
        )

    def patch(self, request, authorId: int):
        # Partial update (via partial=True). Fields which are not provided are not updated.
        author = self._get_object(authorId)
        serializer = self._get_serializer(
            instance=author, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully updated via PATCH method.",
            ),
        )

    def delete(self, request, authorId: int):
        author = self._get_object(authorId)
        author.delete()
        return Response(
            success_response(message="Author successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )
