from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import connection
from .forms import signupForm, signinForm
from .models import signupModelForm,User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site


def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            form = signupModelForm(request.POST)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = signinForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        isMatch = User.objects.filter(email=email).filter(password=password)
        if form.is_valid() and isMatch:
            user = User.objects.get(email=email)
            request.session['userID'] = user.userID
            context = {'user':user}
            return render(request, "profile.html",context)
    else:
        form = signinForm()
    return render(request, 'signin.html', {'form': form})


def profile(request):
    # if request.session.has_key('userID'):
    #     username = request.session['username']
    #     return render(request, 'loggedin.html', {"username" : username})
    return render(request, 'profile.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
