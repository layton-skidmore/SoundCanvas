from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album_name} on {self.artist}"
    
    def get_absolute_url(self):
        return reverse("forum:home")


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=3000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} \n {self.title}"

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    date = models.DateField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.name}'s post under '{self.thread.title}' thread"