from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {
        'customers_info': customers,
        'orders_info': orders,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending
    }

    return render(request, "dashboard.html", context)


def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()

    orders_total = customer.order_set.all().count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders_total
    }

    return render(request, "customer.html",context)


def product(request):
    products = Product.objects.all()

    return render(request, "products.html", {'prodcut_list': products})
