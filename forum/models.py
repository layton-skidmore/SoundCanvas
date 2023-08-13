from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    