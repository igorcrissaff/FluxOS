from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def stock_index(request):
    # Fecht all products
    products = Product.objects.all()

    # Calculate stock value
    stock_value = sum(product.price * product.quantity for product in products)

    # Calculate total stock
    total_stock = sum(product.quantity for product in products)

    # Get products out of stock
    products_out_of_stock = products.filter(quantity=0)

    return render(
        request, 'products.html', 
        {
            'products': products, 
            'stock_value': stock_value,
            'total_stock': total_stock,
            'products_out_of_stock': products_out_of_stock
            })

@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.save()
            return redirect(stock_index, permanent=True)
        
        else:
            return render(request, 'product_form.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(stock_index, permanent=True)
        else:
            return render(request, 'product_form.html', {'form': form})
    else:
        form = ProductForm(instance=product)
        return render(request, 'product_form.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect(stock_index, permanent=True)

@login_required
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

@login_required
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
    
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect(categories_view, permanent=True)