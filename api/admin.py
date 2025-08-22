from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from .forms import CustomAdminAuthForm
from .models import *

# Register your models here.

# Customize admin site: https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#adminsite-objects
class MyAdminSite(admin.AdminSite):
    login_form = CustomAdminAuthForm

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.is_authenticated and request.user.role == USER_ROLES.ADMIN.value

admin_site = MyAdminSite()

admin_site.register(User)
admin_site.register(Blog)
admin_site.register(Author)
admin_site.register(Entry)