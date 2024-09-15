from django.db.models import Max, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector

from utils.servise import get_client_ip
from .forms import SearchForm
from .models import Product, Brands, category, ProductVisit, product_galry
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
        queryset = queryset.select_related('brand')
        queryset = queryset.prefetch_related('category_product')
        search = self.request.GET.get('search')
        if search is not None and search != '':
            queryset = queryset.filter(Q(name__icontains=search)
                                       | Q(short_body__icontains=search)
                                       | Q(body__icontains=search))
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
            queryset = queryset.filter(brand_id__in=brand_ids).distinct()
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
            context['brand_ids'] = brand_ids
        search = self.request.GET.get('search')
        if search is not None and search != '':
            context['search'] = search

        url_category = self.kwargs.get('cate_gory')
        CA = category.objects.filter(is_active=True,is_deleted=False,url_name__iexact=url_category).first()
        context['category'] = CA
        return context


class productDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product/detail_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_id:Product = self.object
        gallery = list(product_galry.objects.filter(product_gallery_id=object_id.id).only('image'))
        gallery.insert(0,object_id)
        context['gallery'] = gallery
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip,user_id=user_id, product_id=object_id.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=object_id.id)
            new_visit.save()

        categories_in_cart = Product.objects.filter(id=object_id.id).values_list('category_product', flat=True)
        related_products = Product.objects.filter(category_product__in=categories_in_cart).exclude(
            id=object_id.id)[:16]
        context['related_products'] = related_products
        return context






