from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User


@receiver(pre_save, sender=User)
def remove_gmail_domain(sender, instance, **kwargs):
    if instance.email and instance.email.endswith('@gmail.com'):
        # حذف دامنه @gmail.com
        instance.username = instance.email.replace('@gmail.com', '')
