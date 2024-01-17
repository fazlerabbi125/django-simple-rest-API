from django.shortcuts import get_object_or_404
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Author
from ..serializers import AuthorSerializer
from utils.common import success_response, failure_response, USER_ROLES


@api_view(["GET", "POST"])
def authorList(request: request.Request):
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
            data = request.data.copy() # get mutable copy of QueryDict
            data["user.role"] = USER_ROLES.MEMBER.value
            serializer = AuthorSerializer(data=data)
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
        return get_object_or_404(
            Author, pk=pk
        )  # first arg can be either Model, Manager, or QuerySet object

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

    def put(self, request: request.Request, authorId: int):
        # Complete update (as partial arg in serializer is not provided or false here). Throws exception if all necessary fields are not present
        author = self._get_object(authorId)
        data = request.data.copy()
        data["user.role"] = USER_ROLES.MEMBER.value
        serializer = self._get_serializer(instance=author, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully updated via PUT method.",
            ),
        )

    def patch(self, request: request.Request, authorId: int):
        # Partial update (via partial=True). Fields which are not provided are not updated.
        author = self._get_object(authorId)
        data = request.data.copy()
        data["user.role"] = USER_ROLES.MEMBER.value
        if author.user.email == data.get("user.email"):
            data.pop("user.email")
        serializer = self._get_serializer(instance=author, data=data, partial=True)
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
