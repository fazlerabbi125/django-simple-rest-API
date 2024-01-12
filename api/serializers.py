from .models import *
from rest_framework import serializers

# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/fields/


class BlogSerializer(serializers.ModelSerializer):
    """
    Object-level custom validation: https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    Field-level custom validation: https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    """

    class Meta:
        model = Blog
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    """
    Overriding the default serializer fields with the same name.
    Instead of the depth meta options, serializers should be used for related fields
    to allow customization for the nested object
    """

    blog = BlogSerializer()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Entry
        fields = "__all__"
        # depth=1 #it allows you to return all the fields of its related field as a nested object instead of just getting their primary key values
