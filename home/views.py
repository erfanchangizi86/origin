from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class header(TemplateView):
    template_name = 'repository/header.html'


class footer(TemplateView):
    template_name = 'repository/footer.html'
