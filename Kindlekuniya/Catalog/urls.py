from django.conf.urls import url, include
from django.contrib.sites.models import Site
from . import views

urlpatterns = [
    # /catalog/ -> catalog homepage
    url(r'^$', views.index, name = 'index'),
    url(r'^search/', include('haystack.urls')),
]
