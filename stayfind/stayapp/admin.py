from django.contrib import admin
from stayapp.models import Product
from .models import UserProfile

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'city', 'price', 'is_active', 'para']
    list_filter=['city', 'is_active']

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)