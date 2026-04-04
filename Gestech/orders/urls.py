from django.urls import path
from . import views

urlpatterns = [
    # Web App URLs
    path('', views.orders_index, name='orders_index'),
    path('order/<str:order_id>/', views.view_order, name='view_order'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/edit/<str:order_id>/', views.edit_order, name='edit_order'),
    path('order/delete/<str:order_id>/', views.delete_order, name='delete_order'),
]