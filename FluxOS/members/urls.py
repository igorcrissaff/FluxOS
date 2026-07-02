from django.urls import path
from . import views

urlpatterns = [
    # Web App URLs
    path('', views.users_index, name='users_index'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/edit/<str:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<str:user_id>/', views.delete_user, name='delete_user'),
]