from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id text post rating'.split()


class PostListSerializer(serializers.ModelSerializer):
    comments = CommentItemSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
    comments1 = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "title text created_date comments comments1 comments_count".split()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comments1(self, post):
        comments = Comment.objects.filter(rating__gt=3, post=post)
        data = CommentItemSerializer(comments, many=True).data
        return data


class CommentValidateSerializer(serializers.Serializer):
    comment = serializers.CharField(max_length=2000)


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=1000)


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)
    password1 = serializers.CharField(max_length=1000)

    def validate_username(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError("Пользователь уже существует")
