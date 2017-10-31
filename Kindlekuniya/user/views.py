from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db import connection
import hashlib
from passlib.hash import pbkdf2_sha256
from .models import SignupModelForm, User, AddressModelForm, Address
from .forms import SignupForm, SigninForm, EditProfileForm, ChangePasswordForm, EmailForm, ForgotPasswordForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        password = request.POST['password']
        email = request.POST['email']
        password = pbkdf2_sha256.hash(password)

        if form.is_valid():
            form = SignupModelForm(request.POST)
            user = form.save(commit=False)
            token = account_activation_token.make_token(user)
            user.is_activated = 'WT'
            user.token = token
            user.password = password
            user.save()

            userr = User.objects.get(email=email)

            form_addr = AddressModelForm()
            form_addr = form_addr.save(commit=False)
            form_addr.addr = request.POST['address']
            form_addr.user_id = userr.user_id
            form_addr.city = request.POST['city']
            form_addr.zip = request.POST['zipcode']
            form_addr.save()

            current_site = get_current_site(request)
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                a=email.send()
                alert = 'Please confirm your email address to complete the registration within 30 minutes.'            
            except:
                alert = 'Email is not valid'            

            return render(request, 'user_response.html', {'alert': alert})
    elif request.session.has_key('user_id'):
        return redirect("/logout")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        user_id = request.session['user_id']
        if form.is_valid():
            user = User.objects.get(user_id = user_id)
            user.firstname = request.POST['firstname']
            user.lastname = request.POST['lastname']
            user.phone_number = request.POST['phone_number']
            user.save()
            return redirect("/user/profile")
    
    elif request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        form = EditProfileForm(initial={'firstname':user.firstname,'lastname':user.lastname,'email':user.email,'phone_number':user.phone_number})
    else:
        return redirect("/user/login")
 
    return render(request, 'edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():    
            password = request.POST['old_password']
            new_password = request.POST['new_password']
            user = User.objects.get(email=request.POST['email'])
            if pbkdf2_sha256.verify(password, user.password):
                user.password = pbkdf2_sha256.hash(new_password)
                user.save()
                return redirect("/user/profile")
            else:
                err = "User or Password is invalid"
                return render(
                    request,
                    'change_password.html',
                    {'form': form, 'err': err}
                )    
        elif request.POST['old_password'] == '':
            return redirect("/user/profile")
            
    elif request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        form = ChangePasswordForm(initial={'email':user.email})
    else:
        return redirect("/user/login")
 
    return render(request, 'change_password.html', {'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token == user.token and not user.token == '':
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():    
                new_password = request.POST['new_password']
                user.password = pbkdf2_sha256.hash(new_password)
                user.token = ''
                user.save()
                return redirect("/user/login")
        else:
            form = ForgotPasswordForm()
        return render(request, 'reset_password.html', {'form': form,'uidb64':uidb64, 'token':token})
    else:
        alert = 'Activation link is invalid!'
        return render(request, 'user_response.html', {'alert': alert})

    


def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():   
            user = User.objects.get(email=request.POST['email'])
            token = account_activation_token.make_token(user)
            user.token = token  
            user.is_activated = 'AC'  
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('forgot_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            mail_subject = 'Reset your password'
            email = EmailMessage(mail_subject, message, to=[request.POST['email']])
            email.send()
            
            alert = 'Please check your email.'
            return render(request, 'user_response.html', {'alert': alert})
    else:
        form = EmailForm()
 
    return render(request, 'forgot_password.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        email = request.POST['email']

        if form.is_valid() and User.objects.get(email=email):
            user = User.objects.get(email=email)
            if user.is_activated == 'AC':
                password = request.POST['password']
                if pbkdf2_sha256.verify(password, user.password):
                    request.session['user_id'] = user.user_id
                    request.session.set_expiry(1800)
                    return redirect("/user/profile")
                else:
                    err = "User or Password is invalid"
                    return render(
                        request,
                        'login.html',
                        {'form': form, 'err': err}
                    )    
            elif user.is_activated == 'WT':
                err = "Please confirm email"
                return render(
                    request,
                    'login.html',
                    {'form': form, 'err': err}
                )
            else:
                err = "User or Password is invalid"
                return render(
                    request,
                    'login.html',
                    {'form': form, 'err': err}
                )

    elif request.session.has_key('user_id'):
        return redirect("/user/logout")
    else:
        form = SigninForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if not request.session.has_key('user_id'):
        return redirect("/user/login")
    elif request.method == 'POST':
        try:
            del request.session['user_id']
        except:
            pass
        return redirect("/user/login")
    else:
        return render(request   , 'logout.html')


def profile(request):
    if request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        addr = Address.objects.get(user_id=user_id)
        context = {'user': user, 'addr': addr}
        return render(request, "profile.html", context)
    else:
        try:
            del request.session['user_id']
        except:
            pass
        form = SigninForm()
        return redirect("/user/login")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token == user.token:
        user.is_activated = 'AC'
        user.save()
        alert = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request, 'user_response.html', {'alert': alert})
    else:
        alert = 'Activation link is invalid!'
        return render(request, 'user_response.html', {'alert': alert})
