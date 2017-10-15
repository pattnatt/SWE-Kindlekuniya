from django.conf.urls import url, include
from django.contrib.sites.models import Site
from . import views

app_name = 'Catalog'

urlpatterns = [
    # /-> catalog homepage
    url(r'^$', views.index, name = 'index'),
    # /search -> catalog search
    url(r'^search/', include('haystack.urls'), name = 'search1'),
    # /detail/(number) -> product's details
    url(r'^detail/(?P<product_id>[0-9]+)/$', views.detail, name = 'detail'),
    # /catagory/(number) -> catagory's product
    url(r'^catagory/(?P<catagory_id>[0-9]+)/$', views.catagory, name = 'catagory'),
    url(r'^view_cart/$', views.view_cart, name = 'view_cart'),
]
