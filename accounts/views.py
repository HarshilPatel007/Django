from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm, UserRegistrationForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from accounts.decorators import *

# Create your views here.


# @login_required(login_url='login')
# @admin_only
def home(request):
    # customers = Customer.objects.all()
    # orders = Order.objects.all()
    #
    # total_customers = customers.count()
    # total_orders = orders.count()
    # orders_delivered = orders.filter(status='Delivered').count()
    # orders_pending = orders.filter(status='Pending').count()
    # orders_out_for_delivery = orders.filter(status='Out for Delivery').count()
    # orders_cancelled = orders.filter(status='Cancelled').count()
    #
    # context = {
    #     'customers_info': customers,
    #     'orders_info': orders,
    #     'total_customers': total_customers,
    #     'total_orders': total_orders,
    #     'orders_delivered': orders_delivered,
    #     'orders_pending': orders_pending,
    #     'orders_out_for_delivery': orders_out_for_delivery,
    #     'orders_cancelled': orders_cancelled
    # }
    #
    # return render(request, "dashboard.html", context)
    return render(request, "index.html")


def page_not_found(request):
    return render(request, "404.html")

# @redirect_anon_user
def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        auth_user = authenticate(request, email=email, password=password)

        if (not (email and email.strip())) or (not (password and password.strip())):
            messages.warning(request, "Please enter your Email OR Password.")
        elif auth_user is not None:
            login(request, auth_user)
            # return redirect('customer', customer_id=auth_user.id)
            return redirect('home')
        else:
            messages.warning(request, "Email OR Password Is Incorrect.")

    context = {

    }

    return render(request, "pages/login.html", context)


def logout_page(request):
    logout(request)

    return redirect('login')


# @redirect_anon_user
def register_page(request):

    data = UserRegistrationForm()

    if request.method == 'POST':
        data = UserRegistrationForm(request.POST)
        if data.is_valid():
            user = data.save()
            # username = data.cleaned_data.get('username')

            # Create Group If not available.
            Group.objects.get_or_create(name='customer')
            Group.objects.get_or_create(name='admin')

            # Add User to a customer group.
            get_group = Group.objects.get(name='customer')
            user.groups.add(get_group)

            # Add user to customer
            Customer.objects.create(user=user, name=user.username, email=user.email)

            messages.success(request, 'Account has been created successfully.')
            return redirect('login')

    context = {
        'user_register_form': data
    }

    return render(request, "pages/register.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
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


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()

    context = {
        'product_list': products
    }

    return render(request, "products.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
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


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
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


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'del_order': order
    }
    return render(request, "delete_order.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def user_profile(request):

    customer = request.user.customer

    orders = request.user.customer.order_set.all()

    orders_total = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders_total,
        'filters': myFilter
    }

    return render(request, "users.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def profile_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form':form
    }

    return render(request, "account_settings.html", context)
