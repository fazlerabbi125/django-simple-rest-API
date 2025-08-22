from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Entry
from ..serializers import EntrySerializer
from utils.common import success_response, SwaggerTags
from drf_spectacular.utils import extend_schema

class EntryViewSet(viewsets.GenericViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    lookup_url_kwarg = "entryId"

    """
    Below are the request methods to implement. The GenericViewSet class inherits from GenericAPIView.
    If you use ModelViewSet, you will get inherited functionality from GenericViewSet and
    all request methods are automatically defined but you can override them 
    """

    @extend_schema(
        summary="Get entries",
        description="Retrieves a list of all entries.",
        operation_id="entry_list",
        responses={
            status.HTTP_200_OK: EntrySerializer(many=True),
        },
        tags=[SwaggerTags.ENTRY.value],
    )
    def list(self, request):
        entries = self.get_queryset()
        serializer = self.serializer_class(entries, many=True)
        return Response(
            success_response(
                data=serializer.data,
                message="Entries successfully fetched.",
            ),
        )

    @extend_schema(
        summary="Create an entry",
        description="Creates a new entry with the given details.",
        operation_id="entry_create",
        request=EntrySerializer,
        responses={
            status.HTTP_201_CREATED: EntrySerializer,
        },
        tags=[SwaggerTags.ENTRY.value],
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Entry successfully created.",
            ),
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Get an entry",
        description="Retrieves the details of a specific entry.",
        operation_id="entry_detail",
        responses={
            status.HTTP_200_OK: EntrySerializer,
        },
        tags=[SwaggerTags.ENTRY.value],
    )
    def retrieve(self, request, entryId: int):
        entry = self.get_object()
        serializer = self.serializer_class(entry)
        return Response(
            success_response(
                data=serializer.data,
                message="Entry successfully fetched.",
            ),
        )

    # def update(self, request, entryId=None):
    #     pass

    @extend_schema(
        summary="Partially update an entry",
        description="Updates an existing entry with the given details.",
        operation_id="entry_patch",
        request=EntrySerializer,
        responses={
            status.HTTP_200_OK: EntrySerializer,
        },
        tags=[SwaggerTags.ENTRY.value],
    )
    def partial_update(self, request, entryId: int):
        entry = self.get_object()
        serializer = self.serializer_class(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Entry successfully updated.",
            ),
        )

    @extend_schema(
        summary="Delete an entry",
        description="Deletes an existing entry.",
        operation_id="entry_delete",
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=[SwaggerTags.ENTRY.value],
    )
    def destroy(self, request, entryId: int):
        entry: Entry = self.get_object()
        entry.delete()
        return Response(
            success_response(message="Entry successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )
