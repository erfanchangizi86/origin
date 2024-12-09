import random

from django.contrib.auth import login,logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, RegistrationLoginForm, OTPForm
from utils.repository_login import RepositoryLogin
from kavenegar import KavenegarAPI

from .models import Profile, User

# Create your views here.
login_user = RepositoryLogin()


class Register(View):
    class_form = RegistrationForm
    template_name = 'suin_login/register.html'

    def get(self, request):
        forms = self.class_form()
        return render(request, self.template_name, {'form': forms})

    def post(self, request):
        forms = self.class_form(request.POST)
        if forms.is_valid():
            data_user = forms.cleaned_data.get('identifier')
            otp = str(random.randint(100000, 999999))
            login_user.register(data_user, otp)
            return redirect('login')
        return render(request, self.template_name, {'form': forms})


class Login(View):
    template_name = 'suin_login/login.html'
    class_form = RegistrationLoginForm
    otp = str(random.randint(100000, 999999))

    def get(self, request):
        forms = self.class_form()
        return render(request, self.template_name, {'form': forms})

    def post(self, request):
        forms = self.class_form(request.POST)
        if forms.is_valid():
            data_user = forms.cleaned_data.get('identifier')
            data_pass = forms.cleaned_data.get('otp')
            user = login_user.login(request, email=data_user, otp=data_pass, form=forms, opt_update=self.otp)
            if user:
                return redirect('products')
        return render(request, self.template_name, {'form': forms})


def log_out(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
