from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, "dashboard.html")


def customer(request):
    return render(request, "customer.html")


def product(request):
    return render(request, "products.html")
