from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from kavenegar import KavenegarAPI, APIException, HTTPException
from account.forms import RegistrationLoginForm
from account.models import User, Profile
from products.forms import CommentForm


class RepositoryLogin:

    def register(self, email_or_phone, otp):
        if email_or_phone.isdigit():
            # پیدا کردن یا ایجاد کاربر بر اساس شماره موبایل
            user, created = User.objects.get_or_create(profile__phone_number=email_or_phone)

            # ایجاد یا به‌روزرسانی پروفایل
            profile, profile_created = Profile.objects.get_or_create(user=user,
                                                        defaults={'phone_number': email_or_phone,
                                                                                   'otp': otp})

            if not profile_created:
                profile.otp = otp  # به‌روزرسانی OTP در صورت وجود پروفایل
                profile.phone_number = email_or_phone
                profile.save()
            try:
                api = KavenegarAPI('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                params = {'sender': '10008663', 'receptor': email_or_phone, 'message': f'Your OTP is {otp}'}
                response = api.sms_send(params)
            except (APIException, HTTPException) as e:
                return HttpResponse({"error": "Failed to send OTP"}, status=500)

        elif email_or_phone:
            user, created = User.objects.get_or_create(email=email_or_phone)
            profile, created = Profile.objects.get_or_create(user=user, defaults={'otp': otp})
            if not created:
                profile.otp = otp
            profile.save()
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
