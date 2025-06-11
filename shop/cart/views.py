from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Product, Cart, Comment, Comment2
from .forms import CommentForm, GuestCommentForm

# Create your views here.

def products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "products222.html", context=context)

def get_product(request, product_id: int):
    try:
        product = Product.objects.get(pk=product_id)
    except Exception as e:
        return render(request, "404.html")

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = Comment(
                user=request.user,
                product=product,
                content=comment_form.cleaned_data["content"]
            )
            new_comment.save()
            messages.success(request, 'Comment was added')
            return redirect(reverse("product", kwargs={"product_id": product_id}))
        messages.error(request, 'This is an error message.')
        return redirect(reverse("product", kwargs={"product_id": product_id}))

    comments = Comment.objects.filter(product=product)
    comment_form = CommentForm()
    context = {
        "product": product,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "product.html", context=context)



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


def detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Exception as e:
        return render(request, "404.html")

    if request.method == "POST":
        form = GuestCommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment was added')
            return redirect(reverse("product", kwargs={"product_id": pk}))

    comments = Comment2.objects.filter(product=product)
    comment_form = GuestCommentForm()
    context = {
        "product": product,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "product.html", context=context)