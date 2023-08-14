from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    album_cover = models.URLField(blank=True)
    

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(max_length=300)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE)