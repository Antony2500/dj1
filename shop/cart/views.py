from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Product, Cart

# Create your views here.

def products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "products222.html", context=context)


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        person_id = request.POST.get("person_id")

        try:
            new_cart = Cart(user=request.user, product_id=int(product_id))
            new_cart.save()
            messages.success(request, "Fine, Cart was create!")
        except Exception as e:
            print(e)
            messages.error(request, "Ops, something wrong. Plz try later :(")
        finally:
            return redirect("products")