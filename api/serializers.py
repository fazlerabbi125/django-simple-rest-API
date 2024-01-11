from .models import *
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    """
    Overriding the default serializer fields with the same name.
    Instead of the depth meta options, serializers should be used for related fields
    tp allow customization
    """

    blog = BlogSerializer()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Entry
        fields = "__all__"
        # depth=1 #it allows you to return all the fields of a related field instead of just getting their primary key values
