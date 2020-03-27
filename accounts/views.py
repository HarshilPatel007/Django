from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm

# Create your views here.


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    orders_out_for_delivery = orders.filter(status='Out for Delivery').count()
    orders_cancelled = orders.filter(status='Cancelled').count()

    context = {
        'customers_info': customers,
        'orders_info': orders,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
        'orders_out_for_delivery': orders_out_for_delivery,
        'orders_cancelled': orders_cancelled
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

    context = {
        'product_list': products
    }

    return render(request, "products.html", context)


def create_order(request):
    form = OrderForm()

    if request.method == 'POST':

        data = OrderForm(request.POST)
        if data.is_valid():
            data.save()
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, "order.html", context)


def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)

    if request.method == 'POST':

        data = OrderForm(request.POST, instance=order)
        if data.is_valid():
            data.save()
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, "order.html", context)


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'del_order': order
    }
    return render(request, "delete_order.html", context)
