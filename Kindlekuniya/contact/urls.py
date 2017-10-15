from django.conf.urls import url, include
from django.contrib.sites.models import Site
from . import views

app_name = 'contact'

urlpatterns = [
    # /contact/ -> contact page
    url(r'^$', views.index, name = 'index'),

]
