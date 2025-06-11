from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    photo = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment2(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Оголошення')
    author = models.CharField(max_length=30, verbose_name= 'Автор')
    content = models.TextField(verbose_name='Зміст')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Виводити на екран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')
    class Meta:
        verbose_name_plural = 'Коментарі'
        verbose_name = 'Коментар'
        ordering = ['created_at']
