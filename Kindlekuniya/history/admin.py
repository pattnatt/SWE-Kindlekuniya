from django.contrib import admin

from .models import HistEntry, HistData

admin.site.register(HistEntry)
admin.site.register(HistData)
