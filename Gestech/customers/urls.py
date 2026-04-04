from django.urls import path
from . import views

urlpatterns = [
    # Web App URLs
    path('', views.customers_index, name='customers_index'),
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/edit/<str:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customer/delete/<str:customer_id>/', views.delete_customer, name='delete_customer'),
]