from django.forms import ModelForm
from .models import Category, Thread, Post

class CategoryForm(ModelForm):
  class Meta:
    model = Category
    fields = ['album_name', 'artist']

class ThreadForm(ModelForm):
  class Meta:
    model = Thread
    fields = ['title', 'text']

class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ['text']