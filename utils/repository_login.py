from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from account.forms import RegistrationLoginForm
from account.models import User
from products.forms import CommentForm


class RepositoryLogin:

    def register(self, email_or_phone, password):
        # if email_or_phone.isdigit():
        #     user = User(phone_number=email_or_phone)
        #     user.set_password(password)
        #     user.save()
        if email_or_phone:
            user = User(email=email_or_phone)
            user.set_password(password)
            user.save()
        return HttpResponse('ok')

    def login(self,request:HttpRequest,email,password,form:RegistrationLoginForm):
        user:User = User.objects.filter(email__iexact=email).first()
        if user is not None:
            if user.check_password(password):
                login(request,user)
                user.is_active = True
                user.save()
                return user
            else:
                form.add_error('password','پسورد رو اشتباه وارد کردی')






class Comment_form(View):
    def get(self,request:HttpRequest):
        forms = CommentForm(self.request.GET)
        return render(request,'product/detail_product.html',context={'form':forms})
    def post(self,request:HttpRequest):
        forms = CommentForm(self.request.POST)
        if forms.is_valid():
            text=forms.cleaned_data.get('text')

        return render(request,'product/detail_product.html',context={'form':forms})
