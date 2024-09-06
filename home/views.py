from urllib import request

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView
from products.forms import SearchForm
from products.models import Product


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home_html/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_visit = Product.objects.filter(is_active=True,is_deleted=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:18]

        product_sale = Product.objects.filter(is_active=True,is_deleted=False,is_sale=True)[:18]
        context['product_sale'] = list(product_sale)
        context['product_visit'] = products_visit
        return context


class header(TemplateView):
    template_name = 'repository/header.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search','')
        if search is not None and search != "":
            context['search'] = search
        return context

class footer(TemplateView):
    template_name = 'repository/footer.html'
