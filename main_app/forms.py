from django import forms
from .models import Review, Album

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'artist_name', 'album_cover']

