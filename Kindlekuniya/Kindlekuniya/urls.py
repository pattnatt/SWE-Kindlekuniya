from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf.urls.static import static
from templateModule import views as template_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', include('Catalog.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^history/', include('history.urls')),
    url(r'^index/',template_views.index, name='index'),
    url(r'^genres/',template_views.genres, name='genres'),
    url(r'^book/',template_views.book, name='book'),
    url(r'^contact/',template_views.contact, name='contact'),
]
