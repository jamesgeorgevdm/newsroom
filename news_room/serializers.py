"""
DRF serializers for articles, newsletters, publishers, and authors.

Serializers include nested fields for relational context.
"""

from rest_framework import serializers
from .models import Article, Publisher, CustomUser, Newsletter


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for publisher data."""
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for basic author profile."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for article objects including related author and publisher.

    Used in API endpoints for reading filtered articles.
    """
    publisher = PublisherSerializer()
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'description', 'content',
            'approved', 'created_at', 'updated_at',
            'publisher', 'author'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for newsletter objects including related author and publisher.
    """
    publisher = PublisherSerializer()
    author = AuthorSerializer()

    class Meta:
        model = Newsletter
        fields = [
            'id', 'title', 'content',
            'author', 'publisher', 'created_at'
        ]
