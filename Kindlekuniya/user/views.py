from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import connection
from .forms import SignupForm, SigninForm
from .models import SignupModelForm, User, AddressModelForm, Address
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from passlib.hash import pbkdf2_sha256
import hashlib


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        password = request.POST['password']
        email = request.POST['email']
        enc_password = hashlib.md5(password.encode()).hexdigest()

        if form.is_valid():
            form = SignupModelForm(request.POST)

            user = form.save(commit=False)
            token = account_activation_token.make_token(user)
            user.is_activated = 'WT'
            user.token = token
            user.password = enc_password
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
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            alert = 'Please confirm your email address to complete the registration'
            return render(request, 'user_response.html', {'alert': alert})
    elif request.session.has_key('user_id'):
        return redirect("/logout")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        email = request.POST['email']

        if form.is_valid() and User.objects.get(email=email):
            user = User.objects.get(email=email)
            if user.is_activated == 'AC':
                password = request.POST['password']
                # verify = pbkdf2_sha256.verify(password, user.password)
                # if  verify:
                print(user.user_id)
                if hashlib.md5(password.encode()).hexdigest() == user.password:
                    request.session['user_id'] = user.user_id
                    request.session.set_expiry(1800)
                    return redirect("/")
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
        return redirect("/logout")
    else:
        form = SigninForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if not request.session.has_key('user_id'):
        return redirect("/login")
    elif request.method == 'POST':
        try:
            del request.session['user_id']
        except:
            pass
        return redirect("/login")
    else:
        return render(request, 'logout.html')


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
        return redirect("/login")


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
