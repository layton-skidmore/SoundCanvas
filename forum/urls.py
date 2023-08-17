from django.urls import path
from . import views

app_name = 'forum'
	
urlpatterns = [
	path('', views.CategoryList.as_view(), name='home'),
	path('create/', views.CategoryCreate.as_view(), name='category_create'),
	path('<int:category_id>/', views.details, name='category_details'),
	path('<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),
	path('<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
	path('<int:category_id>/<int:thread_id>/', views.thread_details, name='thread_details'),
	path('<int:category_id>/<int:thread_id>/update/', views.thread_update, name='thread_update'),
	path('<int:category_pk>/<int:pk>/delete/', views.ThreadDelete.as_view(), name='thread_delete'),
	path('<int:category_id>/<int:thread_id>/<int:post_id>/edit/', views.post_update, name='post_update'),
	path('<int:category_pk>/<int:thread_pk>/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),

	
 ]