from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comments')
    rating = models.IntegerField(default=5, null=True)

    def __str__(self):
        return self.text


class LikedPosts(models.Model):
    post = models.ForeignKey(Post, null=True,
                             on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
