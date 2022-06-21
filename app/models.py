from cgitb import text
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


# class User_Information(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     avatar = 

class Post(models.Model):
    '''
        *is_reply* is needed to make sure that post is not reply or comment to another post
    '''
    text = models.TextField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField("Post created date", default=datetime.now)
    published = models.BooleanField("Published",default=False)
    is_reply = models.BooleanField("Reply for post",default=False)
    author = models.ForeignKey(User, verbose_name="Author of post", on_delete=models.CASCADE)
    parent_post = models.ForeignKey("self", verbose_name="Branch parent post", on_delete=models.SET_NULL, null=True, blank=True)

# class Post_File(models.Model):
#     post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)

class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    datetime = models.DateTimeField("liked date", default=datetime.now)

