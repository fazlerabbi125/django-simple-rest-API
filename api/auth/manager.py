from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from utils.common import USER_ROLES

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(email=email, **extra_fields)
        user.set_password(password) # hashes raw password and sets password field
        user.full_clean() # Trigger validation for model fields
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        # create superuser here
        extra_fields["role"] = USER_ROLES.ADMIN.value
        return self.create_user(email, password, **extra_fields)
