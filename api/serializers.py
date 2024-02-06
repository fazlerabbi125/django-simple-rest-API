from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from utils.handle_file import change_filename

# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/fields/
# https://www.django-rest-framework.org/api-guide/relations/


class BlogSerializer(serializers.ModelSerializer):
    """
    Object-level custom validation: https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    Field-level custom validation: https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    """

    class Meta:
        model = Blog
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        validated_data["password"] = make_password(validated_data["password"])
        if "photo" in validated_data:
            validated_data["photo"].name = change_filename(validated_data["photo"])

        return super().create(validated_data)

    def update(self, instance: User, validated_data: dict):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])

        if "photo" in validated_data:
            if instance.photo: instance.photo.delete()
            validated_data["photo"].name = change_filename(validated_data["photo"])

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class AuthorSerializer(serializers.ModelSerializer):
    """
    The depth Meta options allows you to return all the fields of its relational field as a nested object
    instead of just getting their primary key values. However, serializers should be used for relational fields instead
    to allow customization for the nested object. By default, nested serializers support only read-operations.
    If you want to support write-operations to a nested serializer field, you'll need to
    create create() and/or update() methods in order to explicitly specify how the child relationships should be saved
    """

    user = UserSerializer()

    def create(self, validated_data: dict):
        validated_data["user"] = self.fields["user"].create(validated_data.pop("user"))
        return super().create(validated_data)

    def update(self, instance: Author, validated_data: dict):
        self.fields["user"].update(instance.user, validated_data.pop("user"))
        return super().update(instance, validated_data)

    class Meta:
        model = Author
        fields = "__all__"
        # depth=1


class EntrySerializer(serializers.ModelSerializer):
    def to_representation(self, obj: Entry):
        # To get relational fields as nested objects only during read operation
        res = super().to_representation(obj)
        res["blog"] = BlogSerializer(obj.blog).data
        res["authors"] = AuthorSerializer(obj.authors, many=True).data
        return res

    class Meta:
        model = Entry
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Email",
        trim_whitespace=False,
    )
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
    )
