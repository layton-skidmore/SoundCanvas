from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Review, Album

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def profile_index(request):
    albums = Album.objects.all()
    return render(request, 'profile/index.html', {'albums' : albums })

class NewAlbumView(CreateView):
    model = Album
    fields = ['name', 'artist_name']
    template_name = 'main_app/new_album.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)
    
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)