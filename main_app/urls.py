from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
    path('index/', views.profile_index, name='index'),
    path('about/', views.about, name='about'),
    path('new_album/create/', views.NewAlbumView.as_view(), name='new_album'),
 ]