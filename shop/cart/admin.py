from django.contrib import admin

from .models import Product, Cart, Comment

# Register your models here.
@admin.register(Product, Cart, Comment)
class Market(admin.ModelAdmin):
    pass
