from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    path('customer/', views.customer),
    path('product/', views.product)
]