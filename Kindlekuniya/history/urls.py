from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<orderId>[0-9a-f-]+)/$', views.detail, name='details'),
]
