from .models import *
from rest_framework import serializers

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


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    """
    The depth Meta options allows you to return all the fields of its relational field as a nested object
    instead of just getting their primary key values. However, serializers should be used for relational fields instead
    to allow customization for the nested object. By default, nested serializers support only read-operations.
    If you want to support write-operations to a nested serializer field, you'll need to
    create create() and/or update() methods in order to explicitly specify how the child relationships should be saved
    """

    def to_representation(self, obj: Entry):
        # To get relational fields as nested objects only during read operation
        res = super().to_representation(obj)
        res["blog"] = BlogSerializer(obj.blog).data
        res["authors"] = AuthorSerializer(obj.authors, many=True).data
        return res

    class Meta:
        model = Entry
        fields = "__all__"
        # depth=1
