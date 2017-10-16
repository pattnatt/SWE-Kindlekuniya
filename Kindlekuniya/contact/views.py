from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


def index(request):
    title = 'Contact Us'
    form = ContactForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'Message from Customer in Kindlekuniya Website'
        message = '%s %s' % (comment, name)
        email_from = form.cleaned_data['email']
        email_to = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, email_to, fail_silently=True)
        title = "Thanks!"
        confirm_message = "Thanks for the message. We will get right back to you."
        form = None

    context = {
        'title': title,
        'form': form,
        'confirm_message': confirm_message,
    }
    return render(request, 'contact.html', context)
