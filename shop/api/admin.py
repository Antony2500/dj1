from django.contrib import admin

from .models import Item

# Register your models here.
@admin.register(Item)
class Item(admin.ModelAdmin):
    pass