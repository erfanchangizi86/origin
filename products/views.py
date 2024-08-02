from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product


# Create your views here.


class productListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list_product.html'


class productDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product/detail_product.html"
