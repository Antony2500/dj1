from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from .forms import CustomAuthForm, RegistrationForm
from market.models import Person


class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm
    template_name = "login.html"


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if "bog2@gmail.com" == user.email:
                content_type = ContentType.objects.get_for_model(Person)
                permission = Permission.objects.create(
                    codename="can_read",
                    name="Can Read Persons",
                    content_type=content_type,
                )
                user.user_permissions.add(permission)

            return redirect("/")

    form = RegistrationForm()

    return render(request, "register.html", context={"register_form": form})


def logout_user(request):
    logout(request)
    return redirect("/")

