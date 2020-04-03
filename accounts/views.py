from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm, UserRegistrationForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
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


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            auth_user = authenticate(request, username=username, password=password)

            if auth_user is not None:
                login(request, auth_user)
                # return redirect('customer', customer_id=auth_user.id)
                return redirect('home')

            else:
                messages.info(request, 'Username OR Password Is Incorrect.')

        context = {

        }

        return render(request, "login.html", context)


def logout_page(request):
    logout(request)

    return redirect('login')


def register_page(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        user_creation_form = UserRegistrationForm()

        if request.method == 'POST':
            data = UserRegistrationForm(request.POST)
            if data.is_valid():
                data.save()
                messages.success(request, 'Account has been created successfully.')
                return redirect('login')

        context = {
            'user_register_form': user_creation_form
        }

        return render(request, "register.html", context)


@login_required(login_url='login')
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()

    orders_total = customer.order_set.all().count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders_total,
        'filters': myFilter
    }

    return render(request, "customer.html", context)


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()

    context = {
        'product_list': products
    }

    return render(request, "products.html", context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'del_order': order
    }
    return render(request, "delete_order.html", context)
