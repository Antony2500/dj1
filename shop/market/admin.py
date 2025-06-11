from django.contrib import admin

from .models import Person, Musician, Album, Stuff, Order, Product


# Register your models here.

@admin.register(Person, Musician, Album, Order, Product)
class Market(admin.ModelAdmin):
    pass

@admin.register(Stuff)
class MyStuffModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_available')
    list_filter = [
        ("is_available", admin.BooleanFieldListFilter),
    ]
    search_fields = ('name', 'name')
    actions = ['my_custom_action']
    def my_custom_action(self, request, queryset):
        queryset.update(is_available=True)


    # def my_custom_action(self, request, queryset):
    #     for obj in queryset:
    #         obj.is_available = True