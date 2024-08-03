from django.contrib import admin

from products.models import Product,category


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('title','url_name')
    list_filter = ('title','url_name')