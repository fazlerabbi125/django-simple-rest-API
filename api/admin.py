from django.contrib import admin
from .models import *
# Register your models here.

admin.register(User)
admin.register(Blog)
admin.register(Author)
admin.register(Entry)