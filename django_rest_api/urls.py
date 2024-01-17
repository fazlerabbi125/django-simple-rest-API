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
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from django.conf import settings
from django.conf.urls.static import static
from utils.common import failure_response

"""
https://docs.djangoproject.com/en/5.0/topics/http/views/#customizing-error-views
Custom error views for Django excluding rest_framework error responses
You have to set the following for these to take effect:
DEBUG = False

ALLOWED_HOSTS = ['*'] for any host or a list of specific allowed hosts
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


urlpatterns = [
    # Implement custom user backend and ModelAdmin class to use django admin view with custom user model 
    # path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
