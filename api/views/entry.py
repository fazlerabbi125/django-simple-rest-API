from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Entry
from ..serializers import EntrySerializer
from utils.common import success_response


class EntryViewSet(viewsets.GenericViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    lookup_url_kwarg = "entryId"

    """
    Below are the request methods to implement. The GenericViewSet class inherits from GenericAPIView.
    If you use ModelViewSet, you will get inherited functionality from GenericViewSet and
    all request methods are automatically defined but you can override them 
    """

    def list(self, request):
        entries = self.get_queryset()
        serializer = self.serializer_class(entries, many=True)
        return Response(
            success_response(
                data=serializer.data,
                message="Entries successfully fetched.",
            ),
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

    def destroy(self, request, entryId: int):
        entry: Entry = self.get_object()
        entry.delete()
        return Response(
            success_response(message="Entry successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )
