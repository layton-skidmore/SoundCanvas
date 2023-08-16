from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
	
urlpatterns = [
	path('', views.home, name='home'),
    path('index/', views.profile_index, name='index'),
    path('about/', views.about, name='about'),
    path('new_album/create/', views.NewAlbumView.as_view(), name='new_album'),
    path('update_album/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album_update'),
    path('delete_album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('album/<int:pk>/', views.album_detail, name='detail'),
  
 ]
