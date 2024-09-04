from urllib import request

from django.shortcuts import render
from django.views.generic import TemplateView
from products.forms import SearchForm

# Create your views here.


class header(TemplateView):
    template_name = 'repository/header.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class footer(TemplateView):
    template_name = 'repository/footer.html'
