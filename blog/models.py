from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class Blogpost(models.Model):
    date_created = models.DateTimeField()
    title = models.CharField(max_length=160)
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(User)

class Comment(models.Model):
    date_created = models.DateTimeField()
    user = models.ForeignKey(User)
    blogpost = models.ForeignKey(Blogpost)
    body = models.TextField(max_length=160)

