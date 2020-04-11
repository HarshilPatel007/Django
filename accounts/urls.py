from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),
    path('customer/<str:customer_id>/', views.customer, name="customer"),
    path('user/', views.user_profile, name="user_profile"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('product/', views.product, name="product"),
    path('create_order/', views.create_order, name="create_order"),
    path('update_order/<str:order_id>/', views.update_order, name="update_order"),
    path('delete_order/<str:order_id>/', views.delete_order, name="delete_order"),
    path('404/', views.page_not_found, name='page_not_found'),
    path('orders/', views.order_list, name='order_list')
]
