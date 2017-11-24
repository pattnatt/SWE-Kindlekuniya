from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductToCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        max_order_arg = kwargs.pop('max_order')
        current_quantity_arg = kwargs.pop('current_quantity')
        super(ProductToCartForm, self).__init__(*args, **kwargs)
        max_order = int(max_order_arg)
        current_quantity = int(current_quantity_arg)
        if current_quantity <= 0 :
            if max_order > 1:
                self.fields['quantity'] = forms.IntegerField(label='Quantity',
                min_value = 1, max_value = max_order, required = True,
                help_text = "You cannot order more than " + str(max_order) + " items.")
            else :
                self.fields['quantity'] = forms.IntegerField(label='Quantity',
                min_value = 1, max_value = max_order, required = True,
                help_text = "You cannot order more than " + str(max_order) + " item.")
        else :
            if max_order > 1:
                if current_quantity > 1 :
                    self.fields['quantity'] = forms.IntegerField(label='Quantity',
                    min_value = 1, max_value = max_order, required = True,
                    help_text = "You already have " + str(current_quantity) + " items in your cart. <br />" +
                    "You can add " + str(max_order) + " more items or less to your cart.")
                else :
                    self.fields['quantity'] = forms.IntegerField(label='Quantity',
                    min_value = 1, max_value = max_order, required = True,
                    help_text = "You already have " + str(current_quantity) + " item in your cart. <br />" +
                    "You can add " + str(max_order) + " more items or less to your cart.")
            else :
                if current_quantity > 1 :
                    self.fields['quantity'] = forms.IntegerField(label='Quantity',
                    min_value = 1, max_value = max_order, required = True,
                    help_text = "You already have " + str(current_quantity) + " items in your cart. <br />" +
                    "You can add " + str(max_order) + " more item to your cart.")
                else :
                    self.fields['quantity'] = forms.IntegerField(label='Quantity',
                    min_value = 1, max_value = max_order, required = True,
                    help_text = "You already have " + str(current_quantity) + " item in your cart. <br />" +
                    "You can add " + str(max_order) + " more item to your cart.")
