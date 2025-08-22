from rest_framework import status, generics, request
from rest_framework.response import Response
from ..models import Blog
from ..serializers import BlogSerializer
from utils.common import success_response, SwaggerTags
from ..auth import permissions as custom_permissions
from drf_spectacular.utils import extend_schema

class BlogList(generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def check_permissions(self, request: request.Request):
        if request.method == 'POST':
            self.permission_classes = [custom_permissions.IsAdmin]
        return super().check_permissions(request)

    @extend_schema(
        summary="Get blogs",
        description="Retrieves a list of all blogs.",
        operation_id="blog_list",
        responses={
            status.HTTP_200_OK: BlogSerializer(many=True),
        },
        tags=[SwaggerTags.BLOG.value],
    )
    def get(self, request):
        blog_list = self.get_queryset()
        serializer = self.get_serializer(blog_list, many=True)
        return Response(
            success_response(
                data=serializer.data,
                message="Blogs successfully fetched.",
            ),
        )

    @extend_schema(
        summary="Create a blog",
        description="Creates a new blog with the given details.",
        operation_id="blog_create",
        request=BlogSerializer,
        responses={
            status.HTTP_201_CREATED: BlogSerializer,
        },
        tags=[SwaggerTags.BLOG.value],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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

    # kwargs important for getting URL parameter
    @extend_schema(
        summary="Get a blog",
        description="Retrieves the details of a specific blog.",
        operation_id="blog_detail",
        responses={
            status.HTTP_200_OK: BlogSerializer,
        },
        tags=[SwaggerTags.BLOG.value],
    )
    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        serializer = self.get_serializer(blog)
        return Response(
            success_response(
                data=serializer.data,
                message="Blog successfully fetched.",
            ),
        )

    @extend_schema(
        summary="Partially update a blog",
        description="Updates an existing blog partially with the given details.",
        operation_id="blog_patch",
        request=BlogSerializer,
        responses={
            status.HTTP_200_OK: BlogSerializer,
        },
        tags=[SwaggerTags.BLOG.value],
    )
    def patch(self, request, *args, **kwargs):
        blog = self.get_object()
        serializer = self.serializer_class(blog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            success_response(
                data=serializer.data,
                message="Blog successfully updated.",
            ),
        )

    @extend_schema(
        summary="Delete a blog",
        description="Deletes an existing blog.",
        operation_id="blog_delete",
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=[SwaggerTags.BLOG.value],
    )
    def delete(self, request, *args, **kwargs):
        blog: Blog = self.get_object()
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
