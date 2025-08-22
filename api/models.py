from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .auth.manager import CustomUserManager
from utils.common import USER_ROLES
from utils.handle_file import checkFileExists

# Create your models here.
"""
3 ways to define a model in Django:
1) Define it directly in the models.py file
2) https://docs.djangoproject.com/en/5.0/topics/db/models/#organizing-models-in-a-package
3) Define it somewhere completely different and just import the models into the models.py
"""


class Blog(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.TextField()

    def __str__(self):
        return f"{self.pk}-{self.name}"


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField("full name", max_length=255)
    email = models.EmailField("email address", unique=True)
    createdAt = models.DateField(auto_now_add=True)
    photo = models.ImageField(
        "profile photo",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "webp"])
        ],
    )  # by default retrieves file from media root
    role = models.CharField(
        max_length=50,
        choices=[(role.value, role.name.capitalize()) for role in USER_ROLES],
    )
    is_active: bool = True  # Remove inherited User db fields

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]  # fields prompted when creating a user via the createsuperuser management command
    objects: CustomUserManager = CustomUserManager()
    
    def has_perm(self, perm, obj=None):
        if self.role == USER_ROLES.ADMIN.value:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.role == USER_ROLES.ADMIN.value:
            return True
        return super().has_module_perms(app_label)
    
    @property
    def is_staff(self):
        return self.role == USER_ROLES.ADMIN.value
    
    @property
    def is_superuser(self):
        return self.role == USER_ROLES.ADMIN.value

    def __str__(self) -> str:
        return f"{self.pk}-{self.email}"


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk}-{self.user.name}"

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        deleted_user = self.user
        deleted_user.delete()
        return super().delete(*args, **kwargs)


class Entry(models.Model):
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField("date published", auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(to=Author)
    number_of_comments = models.IntegerField(default=0)
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10, message="Rating cannot be above 10"),
            MinValueValidator(0, message="Rating cannot be below 0"),
        ],
    )

    class Meta:
        ordering = ["pub_date"]


# https://docs.djangoproject.com/en/5.0/topics/signals/
# https://docs.djangoproject.com/en/5.0/ref/signals/
@receiver(post_delete, sender=User)
def post_delete_user_photo(sender, instance: User, *args, **kwargs):
    """Delete file field when model instance or queryset is deleted"""
    if instance.photo and checkFileExists(instance.photo.path):
        instance.photo.delete()