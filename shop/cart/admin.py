from django.contrib import admin

from .models import Product, Cart

# Register your models here.
@admin.register(Product, Cart)
class Market(admin.ModelAdmin):
    pass
