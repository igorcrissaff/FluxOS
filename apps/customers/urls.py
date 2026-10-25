from django.urls import path

from . import views

urlpatterns = [
    path('', views.customers_index, name='customers_index'),
    path('customer/view/<int:customer_id>/', views.view_customer, name='view_customer'),
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customer/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
]
