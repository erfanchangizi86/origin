from django.contrib import admin

from products.models import Product, category, Brands, product_galry, comment
from .models import ProductVisit


@admin.action(description='صفر کردن قیمت محصول')
def price_to_zero(modeladmin, request, queryset):
    for a in queryset:
        a.price = 0
        a.save()


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    list_filter = ('name', 'price',)
    search_fields = ('name', 'price')
    actions = [price_to_zero]


@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_name')
    list_filter = ('title', 'url_name')
    search_fields = ('title', 'url_name')


@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_name')
    list_filter = ('title', 'url_name')
    search_fields = ('title', 'url_name')


@admin.register(comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('is_active','text')
    list_filter = ('is_active','text','times')


admin.site.register(ProductVisit)

admin.site.register(product_galry)
