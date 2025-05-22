from django.contrib import admin

from .models import Person, Musician, Album, Stuff, Order, Product


# Register your models here.

@admin.register(Person, Musician, Album, Stuff, Order, Product)
class Market(admin.ModelAdmin):
    pass
