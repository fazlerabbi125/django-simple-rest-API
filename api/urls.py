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
from django.urls import path
from .views.author import *
from .views.blog import *

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
]
