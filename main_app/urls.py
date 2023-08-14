from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
	
urlpatterns = [
	path('', views.home, name='home'),
    path('index/', views.profile_index, name='index'),
    path('about/', views.about, name='about'),
    path('new_album/create/', views.NewAlbumView.as_view(), name='new_album'),
    path('accounts/signup/', views.signup, name='signup'),
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)