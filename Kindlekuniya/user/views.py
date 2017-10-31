from .forms import SignupForm, SigninForm, EditProfileForm, ChangePasswordForm, ResetPasswordForm, ForgotPasswordForm, ResendEmailForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import SignupModelForm, User, AddressModelForm, Address
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse,HttpResponseRedirect
from django.db import connection
from passlib.hash import pbkdf2_sha256

def email_activation(user):
    domain = 'http://localhost:8000'
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    message = render_to_string('active_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })
    mail_subject = 'Activate your account.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            password = pbkdf2_sha256.hash(password)
            
            form_signup = SignupModelForm(request.POST)
            # it will return an object that hasn’t yet been saved to the database
            user = form_signup.save(commit=False)
            user.password = password
            user.save()

            form_address = AddressModelForm()
            address = form_address.save(commit=False)
            address.addr = request.POST['address']
            address.city = request.POST['city']
            address.zipcode = request.POST['zipcode']
            address.user = user
            address.save()

            email_activation(user)
            alert = 'Please confirm your email address to complete the registration.'            
            return render('user_response.html', {'alert': alert})

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
            user = User.objects.get(id = user_id)
            user.firstname = request.POST['firstname']
            user.lastname = request.POST['lastname']
            user.phone_number = request.POST['phone_number']
            user.save()
            return HttpResponseRedirect("/user/profile")
    
    elif request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        form = EditProfileForm(initial={'firstname':user.firstname,'lastname':user.lastname,'email':user.email,'phone_number':user.phone_number})
    else:
        return HttpResponseRedirect("/user/login")
 
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
                return HttpResponseRedirect("/user/profile")
            else:
                err = "User or Password is invalid"
                return render(
                    request,
                    'change_password.html',
                    {'form': form, 'err': err}
                )    
        elif request.POST['old_password'] == '':
            return HttpResponseRedirect("/user/profile")
            
    elif request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        form = ChangePasswordForm(initial={'email':user.email})
    else:
        return HttpResponseRedirect("/user/login")
 
    return render(request, 'change_password.html', {'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token == user.token and not user.token == '':
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():    
                new_password = request.POST['new_password']
                user.password = pbkdf2_sha256.hash(new_password)
                user.token = ''
                user.save()
                return HttpResponseRedirect("/user/login")
        else:
            form = ResetPasswordForm()
        return render(request, 'reset_password.html', {'form': form,'uidb64':uidb64, 'token':token})
    else:
        alert = 'Activation link is invalid!'
        return render(request, 'user_response.html', {'alert': alert})

    


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
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
        form = ForgotPasswordForm()
 
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
                    request.session['user_id'] = user.id
                    request.session.set_expiry(1800)
                    return HttpResponseRedirect("/user/profile")
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
        return HttpResponseRedirect("/user/logout")
    else:
        form = SigninForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if not request.session.has_key('user_id'):
        return HttpResponseRedirect("/user/login")
    elif request.method == 'POST':
        try:
            del request.session['user_id']
        except:
            pass
        return HttpResponseRedirect("/user/login")
    else:
        return render(request   , 'logout.html')


def profile(request):
    if request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        addr = Address.objects.get(user_id=user_id)
        context = {'user': user, 'addr': addr}
        return render(request, "profile.html", context)
    else:
        try:
            del request.session['user_id']
        except:
            pass
        form = SigninForm()
        return HttpResponseRedirect("/user/login")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_activated = 'AC'
        user.save()
        alert = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request, 'user_response.html', {'alert': alert})
    else:
        if user.is_activated == 'Active':
            alert = "Your account is activated."
        else:
            return HttpResponseRedirect("/user/resend_email")

def resend_email(request):
    success = False
    err = False
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():   
            user = User.objects.get(email=request.POST['email'])
            user.is_activated = 'WT'
            user.save()
            email_activation(user)
            success = 'Please confirm your email address to complete the registration.'
    else:
        form = ForgotPasswordForm()
        err = 'Your activation link is a invalid.'
    return render(request, 'resend_email.html', {'form': form,'err':err,'success':success})