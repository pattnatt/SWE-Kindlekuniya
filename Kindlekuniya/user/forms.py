from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import signupModelForm,User

class signupForm(forms.Form):
    email = forms.EmailField(required=True, max_length=128)
    firstname = forms.CharField(required=True, max_length=128)
    lastname = forms.CharField(required=True, max_length=128)
    password = forms.CharField(
        required=True, min_length=8, max_length=128, widget=forms.PasswordInput, validators=[RegexValidator(regex='^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$', message ='Password must contain at least one alphabet and one digit')])
    confirm_password = forms.CharField(
        required=True, max_length=128, widget=forms.PasswordInput)
    phone_number = forms.CharField(required=True, max_length=10, min_length=10, validators=[RegexValidator(
        regex='^[0-9]*$', message='Phone number must be numeric 0-9 and Please lengthen phone number to 10.'), ])

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email is already taken.")
        return self.cleaned_data

class signinForm(forms.Form):
    email = forms.EmailField(required=True, max_length=128)
    password = forms.CharField(
        required=True, max_length=128, widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = forms.CharField(required=True, min_length=8, max_length=128, widget=forms.PasswordInput, validators=[RegexValidator(regex='^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$', message ='Password must contain at least one alphabet and one digit')])
        if not User.objects.filter(email=email):
            raise forms.ValidationError("Email or Password is invalid.")
        return self.cleaned_data

    