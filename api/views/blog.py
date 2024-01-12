from rest_framework import status, generics
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from utils.common import success_response

class BlogList(generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        blog_list = self.get_queryset()
        serializer = self.get_serializer(blog_list, many=True)
        return Response(
            success_response(
                data=serializer.data,
                message="Blogs successfully fetched.",
            ),
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Blog successfully created.",
            ),
            status=status.HTTP_201_CREATED,
        )


class BlogDetail(generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_url_kwarg = "blogId"
    # lookup_field = 'pk'

    #kwargs important for getting URL parameter
    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        serializer = self.get_serializer(blog)
        return Response(
            success_response(
                data=serializer.data,
                message="Blog successfully fetched.",
            ),
        )

    def patch(self, request, *args, **kwargs):
        blog = self.get_object()
        serializer = self.get_serializer(blog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Blog successfully updated.",
            ),
        )

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.delete()
        return Response(
            success_response(message="Blog successfully deleted."),
            status=status.HTTP_204_NO_CONTENT,
        )

    # from django.http import Http404
    # def handle_exception(self, exc):
    #     # Overriding parent exeception handler
    #     if isinstance(exc, Http404):
    #         return Response(
    #             failure_response(
    #                 message="Blog not found",
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     return super().handle_exception(exc)
