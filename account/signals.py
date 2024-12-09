from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from account.models import User, Profile


@receiver(pre_save, sender=User)
def remove_gmail_domain(sender, instance, **kwargs):
    # if instance.email and instance.email.endswith('@gmail.com'):
    #     # حذف دامنه @gmail.com
    #     instance.username = instance.email.replace('@gmail.com', '')
    pass

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        # اگر پروفایل وجود ندارد، آن را ایجاد کنید
        Profile.objects.create(user=instance)
    else:
        # هنگام به‌روزرسانی کاربر، پروفایل را ذخیره کنید
        instance.profile.save()