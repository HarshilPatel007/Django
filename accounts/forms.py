from django.forms import ModelForm
from .models import *

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__' # ['customer', 'product', 'date_created', ...] we can add individual fields as well.


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
