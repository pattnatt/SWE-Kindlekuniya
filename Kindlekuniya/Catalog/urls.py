from django.conf.urls import url, include
from django.contrib.sites.models import Site
from . import views

app_name = 'Catalog'

urlpatterns = [
    # /catalog/ -> catalog homepage
    url(r'^$', views.index, name = 'index'),
    # /catalog/search -> catalog search
    url(r'^search/', include('haystack.urls')),
    # /catalog/details/(number) -> product's details
    url(r'^detail/(?P<product_id>[0-9]+)/$', views.detail, name = 'detail'),
]
