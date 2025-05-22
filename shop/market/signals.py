from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.utils.text import slugify

from .models import Product

order_completed = Signal()

@receiver(order_completed)
def handle_order_completed(sender, order, **kwargs):
    send_mail(
        subject="Your order approved",
        message=f"Tnx for trust. Your order is {order.id}",
        from_email=sender,
        recipient_list=[order.user.email]
    )


@receiver(pre_save, sender=Product)
def add_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)