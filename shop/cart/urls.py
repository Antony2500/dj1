from django.urls import path

from .views import add_to_cart, products, get_product

urlpatterns = [
    path("products2", products, name="products"),
    path("add_to_cart", add_to_cart, name="add_to_cart"),
    path("product/<int:product_id>", get_product, name="product")
]