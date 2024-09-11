from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Order, OrderDetail

from products.models import Product


# Create your views here..update(count=count)
class add_to_products(View):
    def get(self, request: HttpRequest):
        count = int(request.GET.get('count'))
        prod_uct_id = int(request.GET.get('ProductId'))
        user = request.user
        if user.is_authenticated:
            product = Product.objects.filter(id=prod_uct_id,is_active=True,is_deleted=False).first()
            if product is not None:
                order, crea = Order.objects.get_or_create(is_paid=False,user_id=user.id)
                current_order_detail = order.orderdetail_set.filter(product_id=prod_uct_id).first()
                if current_order_detail is not None:
                    current_order_detail.count += count
                    current_order_detail.save()
                else:
                    new_detail = OrderDetail(order_id=order.id, product_id=prod_uct_id, count=count)
                    new_detail.save()
                return JsonResponse({'title': 'با موفقیت محصول به سبد خرید شما اضافه شد.', 'icons': 'success'})
            else:
                return JsonResponse({'title': 'این محصول وجود ندارد.', 'icons': 'error'})
        else:
            return JsonResponse({'title': 'ابتدا بایستی لاگین کنید.', 'icons': 'error'})
