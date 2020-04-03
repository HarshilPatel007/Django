from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('customer/<str:customer_id>/', views.customer, name="customer"),
    path('product/', views.product, name="product"),
    path('create_order/', views.create_order, name="create_order"),
    path('update_order/<str:order_id>/', views.update_order, name="update_order"),
    path('delete_order/<str:order_id>/', views.delete_order, name="delete_order")
]
