from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class MyBackend(BaseBackend):
    def authenticate(self, request, token=None):
        # Check the token and return a user.
        pass