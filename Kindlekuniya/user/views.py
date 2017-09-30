from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import connection
from .forms import signupForm, signinForm
from .models import signupModelForm,User,addressModelForm,Address
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
        form = signupForm(request.POST)        
        password = request.POST['password']
        email = request.POST['email']
        enc_password= hashlib.md5(password.encode()).hexdigest()
        
        if form.is_valid():
            form = signupModelForm(request.POST)
            
            user = form.save(commit=False)
            token = account_activation_token.make_token(user)
            user.isActivated = False
            user.token = token
            user.password = enc_password
            user.save()

            userr = User.objects.get(email=email)

            formAddr = addressModelForm()
            formAddr = formAddr.save(commit=False)
            formAddr.addr = request.POST['address']
            formAddr.userID = userr.userID          
            formAddr.city = request.POST['city']
            formAddr.zip = request.POST['zipcode']
            formAddr.save()

            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            alert = 'Please confirm your email address to complete the registration'
            return render(request,'user_response.html',{'alert':alert})
    elif request.session.has_key('userID'):
        return redirect("/logout")
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = signinForm(request.POST)
        email = request.POST['email']
    
        if form.is_valid() and User.objects.get(email=email):
            user = User.objects.get(email=email)
            if user.isActivated:
                password = request.POST['password']
                # verify = pbkdf2_sha256.verify(password, user.password)
                # if  verify:
                print (user.userID)
                if hashlib.md5(password.encode()).hexdigest() == user.password:
                    request.session['userID'] = user.userID
                    request.session.set_expiry(1800)
                    return redirect("/profile")
            else:
                err = "Please confirm email"
                return render(request, 'login.html', {'form': form,'err':err})   

    elif request.session.has_key('userID'):
        return redirect("/logout")
    else:
        form = signinForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if not request.session.has_key('userID'):
        return redirect("/login")
    elif request.method == 'POST':
        try:
            del request.session['userID']
        except:
            pass
        return redirect("/login")
    else:
        return render(request, 'logout.html')

def profile(request):
    if request.session.has_key('userID'):
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        addr = Address.objects.get(userID=userID)
        context = {'user':user,'addr':addr}
        return render(request, "profile.html",context)
    else:
        try:
            del request.session['userID']
        except:
            pass
        form = signinForm()
        return redirect("/login")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token == user.token:
        user.isActivated = True
        user.save()
        alert = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request,'user_response.html',{'alert':alert})
    else:
        alert = 'Activation link is invalid!'
        return render(request,'user_response.html',{'alert':alert})
        
