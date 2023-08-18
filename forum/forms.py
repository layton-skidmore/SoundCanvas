from django.forms import ModelForm, Textarea
from .models import Category, Thread, Post


class ThreadForm(ModelForm):
  class Meta:
    model = Thread
    fields = ['title', 'text']
    widgets = {
            'text': Textarea(attrs={'class': 'mt-3'}),
        }

class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ['text']
    widgets = {
            'text': Textarea(attrs={'placeholder': 'Anything to add...?'}),
        }
    labels = {
            'text': '',
        }