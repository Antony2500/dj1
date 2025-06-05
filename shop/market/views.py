import time
import traceback
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, get_connection, EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest, StreamingHttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Max, Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from django.core.paginator import Paginator

from .models import Person, Stuff, Order
from .forms import PersonForm, PersonModelForm, GetAllPersonForms, CreateNewPersonForms, LoginForm
from .signals import order_completed


def index(request):

    context = {
        "title": "main"
    }

    return render(request, 'index.html', context)



def get_person_by_pk(request, pk: int):
    try:
        person = Person.objects.get(pk=pk)
        return HttpResponse(f"{person}")
    except ObjectDoesNotExist:
        return HttpResponse(f"error: Person with {pk} does not exists")

def get_person_by_surname(request, surname: str):
    person = Person.objects.get(last_name=surname)
    return HttpResponse(f"{person}")


def get_or_create_person(request, pk:int):
    person = Person.objects.get_or_create(
        pk=pk,
        defaults={
            "first_name": "John",
            "last_name": "Sina"
        }
    )

    return HttpResponse(f"{person}")


def change_surname(request, pk: int, surname: str):
    try:
        person = Person.objects.get(pk=pk)

        person.last_name = surname
        person.save()

        return HttpResponse(f"New surname for user - {person.first_name}, {person.last_name}")

    except ObjectDoesNotExist:
        return HttpResponseBadRequest(
            {
                "error": f"Person with {pk} does not exists",
                "traceback": traceback.format_exc()
            }
        )


def create_person(request):
    p = Person(first_name="Patrick", last_name="Saint")

    p.save()
    return HttpResponse("Created")


def update_or_create_person(request, name:str):
    person = Person.objects.update_or_create(
        first_name=name,
        defaults={
            "first_name": "Oguzik",
            "last_name": "Lavrov"
        }
    )
    return HttpResponse(f"{person}")


def delete_person(request, pk: int):
    person = Person.objects.get(
        pk=pk,
    )
    person.delete()
    return HttpResponse(f"Deleted person")

def get_all_persons(request):
    persons = Person.objects.aggregate(Min("first_name"))
    print(persons["first_name__min"])
    for person in persons:
        print(person)

    return render(request, "persons.html", context={"persons": persons})


def request_info_check(request):
    info = []

    # Основні атрибути
    info.append(f"Method: {request.method}")
    info.append(f"Scheme: {request.scheme}")
    info.append(f"Path: {request.path}")
    info.append(f"Encoding: {request.encoding}")
    info.append(f"Content-Type: {request.content_type}")
    info.append(f"Content Params: {request.content_params}")
    # GET і POST параметри
    info.append(f"GET params: {dict(request.GET)}")
    info.append(f"POST params: {dict(request.POST)}")

    # Файли
    info.append(f"FILES: {[f.name for f in request.FILES.values()]}")

    # META-поля (тільки кілька, бо їх дуже багато)
    meta_keys = [
        'CONTENT_LENGTH', 'CONTENT_TYPE', 'HTTP_USER_AGENT',
        'HTTP_ACCEPT', 'HTTP_HOST', 'HTTP_REFERER',
        'REMOTE_ADDR', 'REMOTE_HOST', 'REMOTE_USER',
        'QUERY_STRING', 'SERVER_NAME', 'REQUEST_METHOD'
    ]
    for key in meta_keys:
        info.append(f"META[{key}]: {request.META.get(key)}")

    # resolver_match
    info.append(f"Resolver match: {request.resolver_match}")

    # Заголовки (Django 2.2+)
    if hasattr(request, 'headers'):
        headers = '\n'.join([f"{k}: {v}" for k, v in request.headers.items()])
        info.append("Headers:\n" + headers)

    # Додаткові методи
    info.append(f"Host: {request.get_host()}")
    info.append(f"Port: {request.get_port()}")
    info.append(f"Full Path: {request.get_full_path()}")
    info.append(f"Absolute URL: {request.build_absolute_uri()}")
    info.append(f"Is secure: {request.is_secure()}")

    # AJAX-перевірка
    if hasattr(request, 'is_ajax'):  # Застаріле, але покажемо
        info.append(f"Is AJAX: {request.is_ajax()}")

    return HttpResponse("<br>".join(info), content_type="text/html")


def index22(request):
    resp = HttpResponse("Here will be\n", content_type='text/plain; charset=utf-8')
    resp.write('Головна - ')
    resp.writelines(('page\n', 'site\n'))
    resp['keywords'] = 'Python, Django'
    return resp


def stream_view(request):
    def event_stream():
        for i in range(5):
            yield f"data: {i}\n\n"
            time.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


@require_http_methods(["GET", "POST"])
def tutorial(request):
    return HttpResponseRedirect(reverse('get_person_by_pk', kwargs={"pk": 1}))


class AboutAs(TemplateView):
    template_name = "about.html"



def get_all_stuff(request):
    context = {
        'all_stuff': Stuff.objects.all(),
    }

    return render(request, "products222.html", context)


def get_all_product_2(request):
    all_products = Stuff.objects.all()
    paginator = Paginator(all_products, 1)

    if "page" in request.GET:
        page_num = request.GET.get('page', 1)
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    return render(request, "products222.html", {"page": page, "products": page.object_list})


def create_person_form(request):
    if request.method == "POST":
        new_form = PersonModelForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            return redirect("index")

        else:
            messages.warning(request, "Wrond data")

    new_form = PersonModelForm()
    context = {"form": new_form}
    return render(request, "forms.html", context)

def get_all_form_persons(request):
    # if request.method == "POST":
    #     pass
    #
    forms = GetAllPersonForms()
    context = {"forms": forms}
    return render(request, "several_forms.html", context=context)

def create_several_persons(request):
    if request.method == "POST":
        forms = CreateNewPersonForms(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("index")

    forms = CreateNewPersonForms(queryset=Person.objects.none())
    context = {"forms": forms}
    return render(request, "several_forms.html", context=context)


def set_cookies_example(request):
    response = HttpResponse("Cookies were set")

    from datetime import datetime, timedelta

    expires = datetime.utcnow() + timedelta(seconds=10)

    response.set_cookie("key", "secret", expires=expires, secure=False)

    return response


def check_cookies_example(request):

    cookies = request.COOKIES

    if "key" not in cookies:
        return HttpResponse(f"403")

    return HttpResponse(f"Cookies - {cookies}")


def login_test(request):
    username = "not logged in"

    if request.method == "POST":
        # Get the posted form
        MyLoginForm = LoginForm(request.POST)

        if MyLoginForm.is_valid():
            username = MyLoginForm.cleaned_data['username']
        else:
            return HttpResponse("500")

        response = render(request, 'loggedin.html', {"username": username},)

        response.set_cookie('last_connection', datetime.now())
        response.set_cookie('username', datetime.now())

        return response


    MyLoginForm = LoginForm()

    response = render(request, 'login.html', {"form": MyLoginForm})
    return response


def formView(request):
    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username = request.COOKIES['username']

        last_connection = request.COOKIES['last_connection']
        last_connection_time = datetime.strptime(last_connection[:-7],
                                                          "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_connection_time).seconds < 10:
            return render(request, 'loggedin.html', {"username": username})
        else:
            return redirect("login_test")

    else:
        return redirect("login_test")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except Exception:
                        return HttpResponse('Invalid header found.')
                    return redirect ("registration/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required
def me(request):
    print("Before request.user")
    if request.user:
        print("After request.user")
        print(request.user.email)

        user = User.objects.get(email=request.user.email)

        if user.has_perm("Person.can_read"):
            print("There is permission")
            persons = Person.objects.all()
            return persons
        return "403"
    return "404"


def test_session_request(request):
    if request.method == "POST":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            request.session["token"] = "19yry19g7-d1fd-f61vd199t4vgx1gb"
            render(request, "index.html")

        request.session["token"] = "19yry19g7-d1fd-f61vd199t4vgx1gb"
        print(request.session)
        print(request.session["token"])
        return HttpResponseBadRequest("Your browser doesn't support cookies ")

    request.session.set_test_cookie()

    return render(request, "session_lesson.html")


def messages_django(request):
    messages.debug(request, 'This is a debug message.')
    messages.info(request, 'This is an informational message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render(request, 'my_template.html')


def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_completed.send(sender=None, order=order)
    return HttpResponse("Tnx, all work")


def test_email(request):
    send_mail(
        'Subject of the Email',
        'Дякуємо, що зареєструвались.',
        None,
        ['anton.andreiev@hippocraticum.ai'],
        fail_silently=False,
        html_message="""<h2 style="color:#2c7be5">Вітаємо у сервісі!</h2>
        <p>Дякуємо, що <b>зареєструвались</b>.</p>
        <a href="https://example.com" style="padding:8px 16px;
           background:#2c7be5;color:#fff;text-decoration:none;border-radius:4px">
           Перейти на сайт
        </a>
        """
    )
    return HttpResponse("Tnx, all work2")


def test_email2(request):
    with get_connection() as conn:
        m1 = EmailMessage("Hello", "One", to=["a@example.com"])
        m2 = EmailMessage("Hi", "Two", to=["b@example.com"])

        conn.send_messages([m1, m2])


def long_request():
    time.sleep(5)
    all_rows = Person.objects.values()
    return list(all_rows)

def test_cache(request):
    data = cache.get_or_set(
        "persons:all",
        long_request,
        timeout=10
    )
    return JsonResponse(data, safe=False)

@cache_page(60 * 5)
def test_cache2(request):
    all_rows = Person.objects.all()
    return render(request, "cache.html", {"persons": all_rows})