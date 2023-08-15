from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm

# Create your views here.

def details(request, category_id):

    category = Category.objects.get(id=category_id)
    thread_form = ThreadForm()
    
    if request.method == 'POST':

        form = ThreadForm(request.POST)

        if form.is_valid():

            new_thread = form.save(commit=False)
            new_thread.user = request.user
            new_thread.category = category
            new_thread.save()


    return render(request, 'details.html', {
        'category': category,
        'thread_form': thread_form
    })


class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'


class CategoryList(ListView):
    model = Category


def thread_details(request, category_id, thread_id):

    category = Category.objects.get(id=category_id)
    thread = Thread.objects.get(id=thread_id)
    post_form = PostForm()

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.thread = thread
            new_post.save()

    return render(request, 'thread_details.html', {
        'category': category,
        'thread': thread,
        'post_form': post_form
    })

