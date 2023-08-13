from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Review, Album

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def profile_index(request):
    return render(request, 'profile/index.html')

class NewAlbumView(CreateView):
    model = Album
    fields = ['name', 'artist_name']
    template_name = 'main_app/new_album.html'