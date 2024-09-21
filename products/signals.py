from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from products.models import Product, comment


@receiver(pre_save, sender=Product)
def calculate_discount(sender, instance, **kwargs):
    if instance.is_sale:
        discount_amount = instance.price * (instance.discount_percent / 100)
        instance.sale_price = instance.price - discount_amount
    else:
        instance.sale_price = 0


@receiver(pre_save, sender=comment)
def comment_product(sender, instance:comment, **kwargs):
    if instance.is_delete :
        instance.delete()