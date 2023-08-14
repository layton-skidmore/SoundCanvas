from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Album(models.Model):
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Review(models.Model):
    text = models.TextField(max_length=300)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE)