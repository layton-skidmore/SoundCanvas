from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse
from urllib.parse import parse_qs
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_required
def details(request, category_id):

    category = Category.objects.get(id=category_id)
    thread_form = ThreadForm()

    is_users_category = True if category.user.id == request.user.id else False
    print(category.user.id)
    print(request.user.id)
    print(is_users_category)
    
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
        'is_users_category': is_users_category,
    })

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['album_name', 'artist']

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['album_name', 'artist']

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryList(LoginRequiredMixin, ListView):
    model = Category


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/forum'

@login_required
def thread_details(request, category_id, thread_id):

    category = Category.objects.get(id=category_id)
    thread = Thread.objects.get(id=thread_id)
    thread_form = ThreadForm()
    post_form = PostForm()
    is_users_thread = True if category.user.id == request.user.id else False

    if request.method == 'POST':

        json_data = None

        if request.POST.dict() != {}:

            print(request.POST.dict())

            request_dict = request.POST.dict()
            request_json = json.dumps(request_dict)
            json_data = json.loads(request_json)  

        else:
        
            json_data = json.loads(request.body.decode('utf-8'))

        
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
                'username': post.user.username,
                'text': post.text,
                'date': post.date,
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'thread': post.thread.id,
                }
                posts_data.append(post_data)
            
            return JsonResponse({'message': 'Post added successfully', 'posts': posts_data, 'user_id': request.user.id, 'category_id': category.id, 'thread_id': thread.id}, content_type='application/json')


        
        return JsonResponse({'message': 'Post added unsuccessfully'}, content_type='application/json')
        

    return render(request, 'thread_details.html', {
        'category': category,
        'thread': thread,
        'post_form': post_form,
        'thread_form': thread_form,
        'is_users_thread': is_users_thread,
        'user_id': request.user.id,
    })

@login_required
def thread_update(request, category_id, thread_id):


    if request.method == 'POST':

        thread = Thread.objects.get(id=thread_id)
        
        title = request.POST['title']
        text = request.POST['text']



        thread.title = title
        thread.text = text
        thread.save()

        return redirect('forum:thread_details', category_id=category_id, thread_id=thread_id)

class ThreadDelete(LoginRequiredMixin, DeleteView):
    model = Thread
    
    def get_success_url(self):
        category_id = self.object.category.id
        return reverse('forum:category_details', kwargs={'category_id': category_id})

@login_required
def post_update(request, category_id, thread_id, post_id):

    if request.method == 'POST':

        post = Post.objects.get(id=post_id)
        
        text = request.POST['text']

        post.text = text
        post.save()

        return redirect('forum:thread_details', category_id=category_id, thread_id=thread_id)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        category_id = self.object.thread.category.id
        thread_id = self.object.thread.id
        return reverse('forum:thread_details', kwargs={'category_id': category_id, 'thread_id': thread_id})