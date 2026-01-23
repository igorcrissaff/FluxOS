import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from . import crud


def index(request):
    products = crud.list_products()

    return render(
        request,           
        'index.html', 
        {
            'products': products, 
            }
        )

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.save()
            return redirect(index, permanent=True)
        
        else:
            return render(request, 'product.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(index, permanent=True)
        else:
            return render(request, 'product.html', {'form': form})
    else:
        form = ProductForm(instance=product)
        return render(request, 'product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect(index, permanent=True)

def categories_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category.save()
            return redirect(categories_view, permanent=True)
        
        else:
            return render(request, 'categories.html', {'form': form})
        
    form = CategoryForm()
    return render(request, 'categories.html', {'form': form, 'categories': categories})

def edit_category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(categories_view, permanent=True)
        else:
            return render(request, 'categories.html', {'form': form, 'categories': categories})
    else:
        form = CategoryForm(instance=category)
        return render(request, 'categories.html', {'form': form, 'categories': categories})
    
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect(categories_view, permanent=True)