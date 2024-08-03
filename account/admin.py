from django.contrib import admin

from account.models import User


# Register your models here.
@admin.register(User)
class admin_user(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')



