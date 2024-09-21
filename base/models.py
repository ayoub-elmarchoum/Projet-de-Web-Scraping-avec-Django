from django.contrib.auth.models import *
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
import requests
import reverse
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
import pyshorteners




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    
    def __str__(self):
        return self.user.username

# the scraped _data model

# class ScrapedData(models.Model):
#     website_url = models.URLField(max_length=2000)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     element_type = models.CharField(default='', max_length=10, choices=[
#                                     ('text', 'Text'), ('image', 'Image'), ('link', 'Link')])
#     element_selector = models.CharField(max_length=100, default='')
#     scraped_data = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         s = pyshorteners.Shortener()
#         self.website_url = s.tinyurl.short(self.website_url)
#         return self.website_url


class ScrapedData(models.Model):
    name_url = models.CharField(null = True ,max_length=100)
    website_url = models.URLField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.name_url)
