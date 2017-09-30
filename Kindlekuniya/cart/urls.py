from django.conf.urls import url

from . import views

app_name = 'cart' 
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='cart'),
    url(r'^results/$', views.ResultsView.as_view(), name='results'),
]
