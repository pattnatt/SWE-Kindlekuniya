from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf.urls.static import static
from templateModule import views as template_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Catalog.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^history/', include('history.urls')),
]
