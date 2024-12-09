from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from account.models import User
from order_module.models import Order, OrderDetail
from products.models import Product
from user_profile.forms import ProfileForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class order_cart(View):
    def get(self, request):
        current_order, created = (Order.objects.prefetch_related('orderdetail_set').get_or_create
                                  (is_paid=False, user_id=request.user.id))

        count = current_order.orderdetail_set.count()
        ordered_products = current_order.orderdetail_set.values_list('product_id', flat=True)
        categories_in_cart = Product.objects.filter(id__in=ordered_products).values_list('category_product', flat=True)
        related_products = Product.objects.filter(category_product__in=categories_in_cart).exclude(
            id__in=ordered_products)

        return render(request, 'user_profile/carts_shope.html', context={'orders': current_order, "count": count,
                                                                         'product': related_products})


@login_required()
def change_min_mix(request):
    i_d = int(request.GET.get('id'))
    state = request.GET.get('value')
    id_order: OrderDetail = OrderDetail.objects.filter(id=i_d, order__is_paid=False,
                                                       order__user_id=request.user.id).first()
    if id_order is not None:
        if state == 'increase':
            id_order.count += 1
            id_order.save()
        elif state == 'decrease':
            if id_order.count == 1:
                id_order.delete()
            else:
                id_order.count -= 1
                id_order.save()
        else:
            return JsonResponse({
                'status': 'state_invalid'
            })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    count = current_order.orderdetail_set.count()
    ordered_products = current_order.orderdetail_set.values_list('product_id', flat=True)
    categories_in_cart = Product.objects.filter(id__in=ordered_products).values_list('category_product', flat=True)
    related_products = Product.objects.filter(category_product__in=categories_in_cart).exclude(
        id__in=ordered_products)
    context = {'orders': current_order, "count": count, 'product': related_products}
    return JsonResponse({'status': 'ok',
                         'body': render_to_string('user_profile/carts_shope_contend.html', context)})


@login_required()
def remove_to(request):
    i_d = request.GET.get('id')
    if i_d is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })
    id_order, delete = OrderDetail.objects.filter(id=i_d, order__is_paid=False,
                                                  order__user_id=request.user.id).delete()
    if delete == 0:
        return JsonResponse({
            'status': 'not id in product',
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    count = current_order.orderdetail_set.count()
    ordered_products = current_order.orderdetail_set.values_list('product_id', flat=True)
    categories_in_cart = Product.objects.filter(id__in=ordered_products).values_list('category_product', flat=True)
    related_products = Product.objects.filter(category_product__in=categories_in_cart).exclude(
        id__in=ordered_products)
    context = {'orders': current_order, "count": count, 'product': related_products}
    return JsonResponse({'status': 'ok',
                         'body': render_to_string('user_profile/carts_shope_contend.html', context)})


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_profile/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context["user"] = user
        return context


@method_decorator(login_required, name='dispatch')
class my_form_edit(View):
    def get(self, request:HttpRequest):
        forms = ProfileForm(instance=request.user)
        context = {'form': forms}
        return render(request, 'user_profile/edit_profile.html', context)

    def post(self, request: HttpRequest):
        forms = ProfileForm(request.POST,instance=request.user)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                forms.add_error('username', 'این نام کاربری قبلاً انتخاب شده است.')
            else:
                forms.save()
                return redirect('profile')
        context = {'form': forms}
        return render(request, 'user_profile/edit_profile.html', context)



