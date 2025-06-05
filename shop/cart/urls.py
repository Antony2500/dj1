from django.urls import path

from .views import add_to_cart, products

urlpatterns = [
    path("products2", products, name="products"),
    path("add_to_cart", add_to_cart, name="add_to_cart")
]