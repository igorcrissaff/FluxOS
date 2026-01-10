import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductForm
from . import crud


def index(request):
    products = crud.list_products()
    print(products[0])
    return render(request, 'index.html', {'products': products})

def get_product(request):
    raise NotImplementedError("This view is not implemented yet.")

def list_products(request):
    raise NotImplementedError("This view is not implemented yet.")

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

def update_product(request, product_id):
    raise NotImplementedError("This view is not implemented yet.")

def delete_product(request, product_id):
    raise NotImplementedError("This view is not implemented yet.")
