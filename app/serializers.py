from rest_framework import serializers
from .models import Post, Like
from django.contrib.auth.models import User

class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','last_login','last_request']


class PostRetrieveSerializer(serializers.ModelSerializer):
    """Getting post/s"""

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'published', 'is_reply', 'author', 'parent_post']

class PostCreateSerializer(serializers.ModelSerializer):
    """Creating Post"""

    class Meta:
        model = Post
        fields = ['text', 'published', 'is_reply', 'author', 'parent_post']

class LikeSerializer(serializers.ModelSerializer):
    """Getting likes"""

    class Meta:
        model = Like
        fields = "__all__"

class LikeByDaySerializer(serializers.ModelSerializer):
    """Getting likes"""
    day = serializers.DateField()
    count = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['day','count']

class LikeCreateSerializer(serializers.ModelSerializer):
    """Adding like"""

    class Meta:
        model = Like
        fields = ['post', 'user']