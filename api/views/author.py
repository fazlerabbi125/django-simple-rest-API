from rest_framework.request import Request, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from utils.common import success_response, failure_response


@api_view(["GET", "POST"])
def get_author_list_or_create(request: HttpRequest | Request):
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


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def get_author_details_or_update_or_delete(
    request: HttpRequest | Request, authorId: int
):
    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response(
            failure_response(
                message="Author not found",
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    match request.method:
        case "GET":
            serializer = AuthorSerializer(author)
            return Response(
                success_response(
                    data=serializer.data,
                    message="Author successfully fetched.",
                ),
                status=status.HTTP_200_OK,
            )
        case "PUT":
            # Complete update (as partial arg in serializer not provided or is false). Throws exception if all necessary fields are not present
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
                status=status.HTTP_200_OK,
            )
        case "PATCH":
            # Partial update (via partial=True). Fields which are not provided are not updated.
            serializer = AuthorSerializer(
                instance=author, data=request.data, partial=True
            )
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
                status=status.HTTP_200_OK,
            )
        case "DELETE":
            serializer = AuthorSerializer(author)
            author.delete()
            return Response(
                success_response(
                    message="Author successfully deleted.", data=serializer.data
                ),
                status=status.HTTP_200_OK,
            )
