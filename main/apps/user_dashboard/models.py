from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    desc = models.CharField(max_length=255)
    password = models.CharField(max_length=40)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    content = models.TextField(max_length=1000, null=True)
    user_page = models.ForeignKey(User, related_name="profile_comments")
    user_comments = models.ForeignKey(User, related_name="user_comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)