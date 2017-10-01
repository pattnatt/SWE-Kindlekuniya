from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf.urls.static import static
from templateModule import views as template_views
from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Catalog.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^history/', include('history.urls')),
    url(r'^signup/$', user_views.signup, name='signup'),
    url(r'^login/$', user_views.login, name='login'),
    url(r'^logout/$', user_views.logout, name='logout'),
    url(r'^profile/$', user_views.profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
]
