from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, RegistrationLoginForm
from utils.repository_login import RepositoryLogin

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
            data_pass = forms.cleaned_data.get('confirm_password')
            login_user.register(data_user, data_pass)
            return redirect('login')
        return render(request, self.template_name, {'form': forms})


class Login(View):
    template_name = 'suin_login/login.html'
    class_form = RegistrationLoginForm

    def get(self, request):
        forms = self.class_form()
        return render(request, self.template_name, {'form': forms})

    def post(self, request):
        forms = self.class_form(request.POST)
        if forms.is_valid():
            data_user = forms.cleaned_data.get('identifier')
            data_pass = forms.cleaned_data.get('password')
            user = login_user.login(request,email=data_user,password=data_pass,form=forms)
            if user:
                return redirect('products')
        return render(request, self.template_name, {'form': forms})
