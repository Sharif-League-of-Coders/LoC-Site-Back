from rest_framework import serializers

from .models import Post, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'image')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'date', 'banner', 'title', 'text',
                  'author', 'brief_text')
