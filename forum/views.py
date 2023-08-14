from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Category

# Create your views here.

def details(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'details.html', {
        'category': category
    })


class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'


class CategoryList(ListView):
    model = Category