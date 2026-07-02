from django.urls import path
from . import views

urlpatterns = [
    # Web App URLs
    path('', views.stock_index, name='stock_index'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/edit/<str:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<str:product_id>/', views.delete_product, name='delete_product'),

    path('categories/', views.categories_view, name='categories'),
    path('category/edit/<str:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<str:category_id>/', views.delete_category, name='delete_category'),
]