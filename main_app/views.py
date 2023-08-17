from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Review, Album
from .forms import ReviewForm, AlbumForm
from decouple import config
import boto3
import uuid
import os
from botocore.exceptions import NoCredentialsError


# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def profile_index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'profile/index.html', {'albums' : albums })

def album_detail(request, pk):
    album = Album.objects.get(id=pk)
    reviews = Review.objects.filter(album=album)

    user_has_review = False
    if request.user.is_authenticated:
        user_reviews = reviews.filter(user=request.user)
        if user_reviews.exists():
            user_has_review = True

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if not user_has_review:
                review = form.save(commit=False)
                review.album = album
                review.user = request.user
                review.save()
                user_has_review = True

    else:
        form = ReviewForm()

    return render(request, 'profile/album_detail.html', {'album': album, 'reviews': reviews, 'form': form, 'user_has_review': user_has_review})




class AlbumCreate(CreateView):
    form_class = AlbumForm
    success_url = '/index/'
    template_name = 'main_app/album_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        album = form.save(commit=False)

        if 'album_cover' in self.request.FILES:
            album_cover = self.request.FILES['album_cover']
            
            aws_access_key_id = config('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
            s3_bucket = config('S3_BUCKET')
            s3_base_url = config('S3_BASE_URL')
            
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                )

                unique_filename = uuid.uuid4().hex[:6] + album_cover.name[album_cover.name.rfind('.'):]

                s3.upload_fileobj(album_cover, s3_bucket, unique_filename)
                album.album_cover = f"{s3_base_url}{s3_bucket}/{unique_filename}"
            except NoCredentialsError:
                print("Credentials not available")

        album.save()
        return super().form_valid(form)

class AlbumUpdate(UpdateView):
  model = Album
  fields = ['name', 'artist_name']
  # Get success redirect will use the return function to pass the name of a view
  def get_success_url(self) -> str:
     return reverse('detail', kwargs= dict(pk=self.object.pk))

class AlbumDelete(DeleteView):
  model = Album
  success_url = '/index'

class ReviewCreate(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'main_app/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['album_id']
        album = Album.objects.get(pk=album_id)
        context['album'] = album
        return context

    def form_valid(self, form):
        album_id = self.kwargs['album_id']
        album = Album.objects.get(pk=album_id)
        review = form.save(commit=False)
        review.album = album
        review.user = self.request.user 
        return super().form_valid(form)

    def get_success_url(self):
        album_id = self.kwargs['album_id']
        return reverse('detail', kwargs={'pk': album_id})
    
class ReviewDelete(DeleteView):
    model = Review
    success_url = '/album/{}/'  
    
    def get_success_url(self):
        return self.success_url.format(self.object.album.pk)
    
class ReviewUpdate(UpdateView):
    model = Review
    fields = ['text', 'rating']
  
    def get_success_url(self) -> str:
        album_id = self.object.album.pk
        return reverse('detail', kwargs={'pk': album_id})
     
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