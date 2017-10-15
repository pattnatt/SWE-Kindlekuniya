from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductToCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        max_order_arg = kwargs.pop('max_order')
        super(ProductToCartForm, self).__init__(*args, **kwargs)
        max_order = int(max_order_arg)
        self.fields['quantity'] = forms.IntegerField(label='Quantity', min_value = 1, max_value = max_order, required = True, help_text = "You cannot order more than " + str(max_order) + " item(s).")
