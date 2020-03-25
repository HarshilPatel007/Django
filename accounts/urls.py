from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('customer/<str:customer_id>/', views.customer, name="customer"),
    path('product/', views.product, name="product")
]
