from django.db.models import Max
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector
from .models import Product, Brands
from utils.category import get_all_categories
from ffmpeg import input
# Create your views here.



class productListView(ListView):
    """
    This class is for displaying the list of products and for filtering them
    """
    model = Product
    context_object_name = 'products'
    template_name = 'product/list_product.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        start_price = self.request.GET.get('startPrice')
        end_price = self.request.GET.get('endPrice')
        if start_price is not None:
            queryset = queryset.filter(price__gte=start_price)
        if end_price is not None:
            queryset = queryset.filter(price__lte=end_price)

        if queryset:
            queryset = queryset.filter(is_active=True)

        categories = self.kwargs.get('cate_gory')
        if categories:
            queryset = queryset.filter(category_product__url_name__iexact=categories)
        brand_ids = self.request.GET.getlist('brand')
        if brand_ids:
            queryset = queryset.filter(brand_id__in=brand_ids)
        else:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories'] = get_all_categories()
        context['brands'] = Brands.objects.filter(is_active=True)
        max_l = Product.objects.aggregate(Max('price'))
        context['max_price'] = max_l
        context['start_price'] = int( self.request.GET.get('startPrice') or 0)
        context['end_price'] = int(self.request.GET.get('endPrice') or max_l['price__max'])
        brand_ids= self.request.GET.getlist('brand')
        if brand_ids is not None:
            context['filter_brand'] = Brands.objects.filter(id__in=brand_ids)
        return context


class productDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product/detail_product.html"




