from django.urls import path
from . import views

urlpatterns = [
    # Web App URLs
    path('', views.index, name='index'),
    path('get/<str:product_id>/', views.get_product, name='get_product'),
    path('list/', views.list_products, name='list_products'),
    path('create/', views.create_product, name='create_product'),
    path('update/<str:product_id>/', views.update_product, name='update_product'),
    path('delete/<str:product_id>/', views.delete_product, name='delete_product'),
]