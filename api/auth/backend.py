from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomUserBackend(BaseBackend):
    def authenticate(
        self,
        request,
        username: str | None = None,
        password: str | None = None,
        **kwargs
    ):
        # Authenticate custom user
        User = get_user_model()
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = User._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
