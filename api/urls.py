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
from django.urls import path, include
from .views.author import *
from .views.blog import *
from .views.entry import EntryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
"""
DefaultRouter provide a default API root view, that returns a response containing hyperlinks to all the registered list views
to perform API CRUD operations online as well as other behavior:
#https://www.django-rest-framework.org/api-guide/routers/#defaultrouter

Adding router to URL config:
https://www.django-rest-framework.org/api-guide/routers/#usage
https://www.django-rest-framework.org/api-guide/routers/#using-include-with-routers
"""
router.register(r"entries", EntryViewSet, basename="entry")
# first arg in router register sets the prefix used by the path and basename is used as part of route name
# We can also bind ViewSets explicitly: https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly

urlpatterns = [
    path("authors/", authorList, name="author_list_create"),
    path(
        "authors/<int:authorId>/",
        AuthorDetail.as_view(),
        name="author_retrieve_update_delete",
    ),
    path(
        "blogs/",
        BlogList.as_view(),
        name="blog_list_create",
    ),
    path(
        "blogs/<int:blogId>/",
        BlogDetail.as_view(),
        name="blog_retrieve_update_delete",
    ),
    path(
        "", include(router.urls)
    ),  # or simply assign/append router.urls to urlpatterns:
]
