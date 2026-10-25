from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import Category, CategoryForm, Movement, MovementForm, Product, ProductForm


@login_required
def stock_index(request):
    all_products = Product.objects.select_related('category')
    products = all_products
    low_stock_filter = request.GET.get('low_stock') in ('1', 'true')

    if low_stock_filter:
        products = products.filter(available=True, quantity__lte=F('low_stock_threshold'))

    stock_value = sum((product.price * product.quantity for product in all_products), Decimal('0.00'))
    total_stock = all_products.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_products = all_products.filter(
        available=True,
        quantity__lte=F('low_stock_threshold'),
    )
    products_out_of_stock = all_products.filter(quantity=0)
    active_products = all_products.filter(available=True)

    return render(
        request,
        'products.html',
        {
            'products': products,
            'stock_value': stock_value,
            'total_stock': total_stock,
            'low_stock_products': low_stock_products,
            'products_out_of_stock': products_out_of_stock,
            'active_products': active_products,
            'low_stock_filter': low_stock_filter,
        },
    )


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product created successfully.'))
            return redirect('stock_index')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product updated successfully.'))
            return redirect('stock_index')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'product': product})


@login_required
@require_POST
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, _('Product deleted successfully.'))
    return redirect('stock_index')


@login_required
def categories_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category created successfully.'))
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'categories.html', {'form': form, 'categories': categories})


@login_required
def edit_category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category updated successfully.'))
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'categories.html',
        {'form': form, 'categories': categories, 'category': category},
    )


@login_required
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, _('Category deleted successfully.'))
    return redirect('categories')


@login_required
def movements_index(request):
    movements = Movement.objects.select_related('product', 'created_by')
    return render(request, 'movements.html', {'movements': movements})


@login_required
def create_movement(request):
    initial = {}
    product_id = request.GET.get('product')
    if product_id:
        initial['product'] = product_id

    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            movement.save()
            messages.success(request, _('Stock movement registered successfully.'))
            return redirect('movements')
    else:
        form = MovementForm(initial=initial)

    return render(request, 'movement_form.html', {'form': form})
