from django.urls import path

from . import views

urlpatterns = [
    path('', views.stock_index, name='stock_index'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('categories/', views.categories_view, name='categories'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('movements/', views.movements_index, name='movements'),
    path('movements/create/', views.create_movement, name='create_movement'),
]
