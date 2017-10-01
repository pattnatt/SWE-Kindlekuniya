from django.conf.urls import url

from . import views

app_name = 'cart'
urlpatterns = [
    url(r'^$', views.IndexView, name='cart'),
    url(r'^results/$', views.ResultsView, name='results'),
    url(r'^payment/$', views.PaymentView, name='payment'),
]
