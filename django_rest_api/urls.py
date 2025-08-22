"""
URL configuration for django_rest_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from api.admin import admin_site
from django.urls import path, include
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from django.conf import settings
from django.conf.urls.static import static
from utils.common import failure_response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

"""
https://docs.djangoproject.com/en/5.0/topics/http/views/#customizing-error-views
Custom error views for Django excluding rest_framework error responses
You have to set the following for these to take effect:
DEBUG = False

ALLOWED_HOSTS = ['*'] for any host or a list of specific allowed hosts

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) and + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) can be used to serve media and static files in development where DEBUG is set to True. This is not suitable for production use!
Common strageies for doing so includes using whitenoise or doing the following:
https://docs.djangoproject.com/en/5.2/howto/static-files/deployment/
"""


def error_view_closure(
    message: str,
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
):
    def custom_error_view(request: HttpRequest, exception: Exception | None = None):
        return JsonResponse(failure_response(message), status=status)

    return custom_error_view


handler404 = error_view_closure("Not found.", status.HTTP_404_NOT_FOUND)
handler500 = error_view_closure("A server error occurred.")

urlpatterns = (
    [
        # To use django admin view with custom user model, do the following: https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#custom-users-and-django-contrib-admin
        path("admin/", admin_site.urls),
        path("browsable-api-auth/", include("rest_framework.urls")),
        # You can add common path prefix using include()
        # See https://docs.djangoproject.com/en/4.2/ref/urls/#django.urls.include
        path("api/", include([
            path("", include("api.urls")),
            path('schema/', include([
                path('', SpectacularAPIView.as_view(), name='schema'),
                path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
            ])),
        ])),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
