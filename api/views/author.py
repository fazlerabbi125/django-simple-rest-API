from django.shortcuts import get_object_or_404
from rest_framework import status, request, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Author
from ..serializers import AuthorInputSerializer, AuthorSerializer
from utils.common import (
    success_response,
    failure_response,
    USER_ROLES,
    ReqMethods,
    SwaggerTags
)
from drf_spectacular.utils import extend_schema


class AuthorList(APIView):
    model = Author

    def get_parsers(self):
        # Initially self.request is None and will give error if not accessed properly
        if self.request and self.request.method == ReqMethods.POST.value:
            self.parser_classes = [parsers.MultiPartParser]
        return super().get_parsers()

    def _get_serializer(self, *args, input: bool = False, **kwargs):
        if input:
            return AuthorInputSerializer(*args, **kwargs)
        return AuthorSerializer(*args, **kwargs)

    @extend_schema(
        summary="Get authors",
        description="Retrieves a list of all authors.",
        operation_id="author_list",
        responses={
            status.HTTP_200_OK: AuthorSerializer(many=True),
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def get(self, request: request.Request, *args, **kwargs):
        authors = self.model.objects.all()
        serializer = self._get_serializer(authors, many=True)
        return Response(
            success_response(
                data=serializer.data,
                message="Authors successfully fetched.",
            ),
        )

    @extend_schema(
        summary="Create an author",
        description="Creates a new author with the given details.",
        operation_id="author_create",
        request=AuthorInputSerializer,
        responses={
            status.HTTP_201_CREATED: AuthorInputSerializer,
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def post(self, request: request.Request):
        data = request.data.copy()  # get mutable copy of request.data
        # Updating request.data from QueryDict and MultiValueDict due to content-type application/x-www-form-urlencoded and multipart/form-data. For json content-type, you can access via data["user"]["role"] as it returns a dictionary.
        data.update({"user.role": USER_ROLES.AUTHOR.value})
        serializer = self._get_serializer(data=data, input=True)
        if not serializer.is_valid():
            return Response(
                failure_response(
                    errors=serializer.errors,
                    message="The given data was invalid",
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

    def get_parsers(self):
        if self.request and self.request.method in [ReqMethods.PUT.value, ReqMethods.PATCH.value]:
            self.parser_classes = [parsers.MultiPartParser]
        return super().get_parsers()

    def _get_object(self, pk: int):
        return get_object_or_404(
            Author, pk=pk
        )  # first arg can be either Model, Manager, or QuerySet object

    def _get_serializer(self, *args, input=False, **kwargs):
        if input:
            return AuthorInputSerializer(*args, **kwargs)
        return AuthorSerializer(*args, **kwargs)

    @extend_schema(
        summary="Get an author's details",
        description="Retrieves the details of a specific author.",
        operation_id="author_detail",
        responses={
            status.HTTP_200_OK: AuthorSerializer,
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def get(self, request, authorId: int):
        author = self._get_object(authorId)
        serializer = self._get_serializer(author)
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully fetched.",
            ),
        )

    @extend_schema(
        summary="Update an author entirely",
        description="Updates an existing author entirely with the given details.",
        operation_id="author_put",
        request={
            "multipart/form-data": AuthorInputSerializer,
        },
        responses={
            status.HTTP_200_OK: AuthorInputSerializer,
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def put(self, request: request.Request, authorId: int):
        # Complete update (as partial arg in serializer is not provided or false here). Throws exception if all necessary fields are not present
        author = self._get_object(authorId)
        data = request.data.copy()
        data["user.role"] = USER_ROLES.AUTHOR.value
        serializer = self._get_serializer(instance=author, data=data, input=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully updated via PUT method.",
            ),
        )

    @extend_schema(
        summary="Update an author partially",
        description="Updates an existing author partially with the given details.",
        operation_id="author_patch",
        request={
            "multipart/form-data": AuthorInputSerializer,
        },
        responses={
            status.HTTP_200_OK: AuthorInputSerializer,
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def patch(self, request: request.Request, authorId: int):
        # Partial update (via partial=True). Fields which are not provided are not updated.
        author = self._get_object(authorId)
        data = request.data.copy()
        data["user.role"] = USER_ROLES.AUTHOR.value
        if author.user.email == data.get("user.email"):
            data.pop("user.email")
        serializer = self._get_serializer(
            instance=author, data=data, partial=True, input=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Author successfully updated via PATCH method.",
            ),
        )

    @extend_schema(
        summary="Delete an author",
        description="Deletes an existing author.",
        operation_id="author_delete",
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=[SwaggerTags.AUTHOR.value],
    )
    def delete(self, request, authorId: int):
        author = self._get_object(authorId)
        author.delete()
        return Response(
            success_response(message="Author successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )
