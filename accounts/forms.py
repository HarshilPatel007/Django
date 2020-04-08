from django.forms import ModelForm
from .models import *

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__' # ['customer', 'product', 'date_created', ...] we can add individual fields as well.


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth']


    # email = forms.EmailField(required=True, label="Email", max_length=100)
    # first_name = forms.CharField(required=True, label="First Name", max_length=100)
    # last_name = forms.CharField(required=True, label="Last Name", max_length=100)
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     for field_name in self.fields:
    #         field = self.fields.get(field_name)
    #         field.widget.attrs['placeholder'] = field.label
    #         field.label = ''
    #         field.help_text = None


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
