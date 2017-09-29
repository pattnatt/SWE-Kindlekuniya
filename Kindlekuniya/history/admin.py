from django.contrib import admin
from .models import Order,OrderItem,Product,Catagory
# Register your models here.

class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3

class OrderSet(admin.ModelAdmin):
    fieldset = [(None , {'field' : ["date","status","shipMethodID"," payMethod","trackingNo"]})]
    inlines = [ItemInline]

admin.site.register(Order, OrderSet)
admin.site.register(Product)
admin.site.register(Catagory)