from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(
        default=18,
        validators=[
            MinValueValidator(18)
        ]
    )

    def __str__(self):
        return self.first_name

class Musician(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    instrument = models.CharField(max_length=100)

class Album(models.Model):

    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    release_date = models.DateField()

    num_stars = models.IntegerField()


class Stuff(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=257)
    photo = models.CharField(max_length=100)
    price = models.IntegerField()
    is_available = models.BooleanField(default=False)

class ShoppingCart(models.Model):
    date_created = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(Stuff)


class Cart(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)


class Product(models.Model):
    name  = models.CharField(max_length=120)
    slug  = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return "Hello World"
