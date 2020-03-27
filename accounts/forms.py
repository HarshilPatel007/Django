from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__' # ['customer', 'product', 'date_created', ...] we can add individual fields as well.
