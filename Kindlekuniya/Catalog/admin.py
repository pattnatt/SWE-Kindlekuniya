from django.contrib import admin
from .models import Product, Catagory, CatagoryMap

class CatagoryMapInline(admin.TabularInline):
    model = CatagoryMap
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [CatagoryMapInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Catagory)
