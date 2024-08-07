from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector
from .models import Product
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
        if queryset:
            queryset = queryset.filter(is_active=True)
        categories = self.kwargs.get('cate_gory')
        if categories:
            queryset = queryset.filter(category_product__url_name__iexact=categories)
        return queryset

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories'] = get_all_categories()
        return context


class productDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product/detail_product.html"




