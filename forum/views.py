from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.core import serializers
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm
import json

# Create your views here.

def details(request, category_id):

    category = Category.objects.get(id=category_id)
    thread_form = ThreadForm()

    is_users_catergory = True if category.user.id == request.user.id else False
    
    if request.method == 'POST':

        form = ThreadForm(request.POST)

        if form.is_valid():

            new_thread = form.save(commit=False)
            new_thread.user = request.user
            new_thread.category = category
            new_thread.save()


    return render(request, 'category_details.html', {
        'category': category,
        'thread_form': thread_form,
        'is_users_catergory': is_users_catergory,
    })

class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'

class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'


class CategoryList(ListView):
    model = Category


class CategoryDelete(DeleteView):
    model = Category
    success_url = '/forum'


def thread_details(request, category_id, thread_id):

    category = Category.objects.get(id=category_id)
    thread = Thread.objects.get(id=thread_id)
    thread_form = ThreadForm()
    post_form = PostForm()
    is_users_thread = True if category.user.id == request.user.id else False

    if request.method == 'POST':

        json_data = json.loads(request.body)
        text = json_data.get('text')

        form = PostForm({'text': text})

        if form.is_valid():

            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.thread = thread
            new_post.save()

            posts = thread.post_set.all()
            posts_data = []
            for post in posts:
                post_data = {
                'id': post.id,
                'user': post.user.id,
                'text': post.text,
                'date': post.date,
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'thread': post.thread.id,
                }
                posts_data.append(post_data)
            
            return JsonResponse({'message': 'Post added successfully', 'posts': posts_data})


        
        return JsonResponse({'message': 'Post added unsuccessfully'})
        

    return render(request, 'thread_details.html', {
        'category': category,
        'thread': thread,
        'post_form': post_form,
        'thread_form': thread_form,
        'is_users_thread': is_users_thread
    })

def thread_update(request, category_id, thread_id):

    if request.method == 'POST':

        thread = Thread.objects.get(id=thread_id)

        json_data = json.loads(request.body)
        title = json_data.get('title')
        text = json_data.get('text')

        thread.title = title
        thread.text = text
        thread.save()

        thread_data = {
            'title': title,
            'text': text,
        }

        return JsonResponse({'message': 'Thread updated successfully', 'thread': thread_data})

        


