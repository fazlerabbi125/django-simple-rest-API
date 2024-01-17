from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from .auth.manager import CustomUserManager
from utils.common import USER_ROLES

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.TextField()

    def __str__(self):
        return f"{self.pk}-{self.name}"


class Author(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        unique=True,
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk}-{self.user.name}"
    
    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        deleted_user =self.user
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


class User(AbstractBaseUser):
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
    is_active: None = None # Remove inherited User attributes
    last_login: None = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"] #fields prompted when creating a user via the createsuperuser management command
    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return f"{self.pk}-{self.email}"
