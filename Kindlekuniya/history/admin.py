from django.contrib import admin

from .models import HistEntry, HistData

class HistDataInline(admin.TabularInline):
    model = HistData
    extra = 1

class HistEntryAdmin(admin.ModelAdmin):
    inlines = [HistDataInline]

admin.site.register(HistEntry, HistEntryAdmin)
admin.site.register(HistData)
