from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from kavenegar import KavenegarAPI, APIException, HTTPException
from account.forms import RegistrationLoginForm
from account.models import User, Profile
from products.forms import CommentForm
from utils.send_email import send_email


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
                api = KavenegarAPI(
                    '4E6C4F35627041774C6E3246335A6F446B344279544F72716B4173547A416A4F34487742436A31476B36673D')
                params = {'sender': '10004346', 'receptor': email_or_phone, 'message': f'Your OTP is {otp}'}
                response = api.sms_send(params)
            except (APIException, HTTPException) as e:
                print(e)
                return HttpResponse({"error": "Failed to send OTP"}, status=500)


        elif email_or_phone:
            user, created = User.objects.get_or_create(email=email_or_phone)
            # بررسی وجود پروفایل
            try:
                profile = Profile.objects.get(user=user)
                # اگر پروفایل وجود دارد، OTP را به‌روزرسانی می‌کنیم
                profile.otp = otp
            except Profile.DoesNotExist:
                # اگر پروفایل وجود نداشت، پروفایل جدید ایجاد می‌کنیم
                profile = Profile.objects.create(user=user, otp=otp)
            profile.save()
            # send_email('فعالسازی حساب کاربری', user.email, {'user': otp}, 'suin_login/activate_account.html')
        return HttpResponse('ok')

    def login(self, request: HttpRequest, email, otp, form: RegistrationLoginForm, opt_update):
            if email.isdigit():
                user: User = User.objects.filter(profile__phone_number__iexact=email).first()
                if user is not None and user.profile.otp == otp:
                    login(request, user)
                    user.profile.otp = opt_update
                    user.is_active = True
                    user.save()
                    return user
                else:
                    form.add_error('identifier', 'مشخصات اشتباه است')
            elif email:
                user = User.objects.filter(email__iexact=email).first()
                if user is not None and user.profile.otp == otp:
                    login(request, user)
                    user.profile.otp = opt_update
                    user.is_active = True
                    user.save()
                    return user
                else:
                    form.add_error('identifier', 'مشخصات اشتباه است')


class Comment_form(View):
    def get(self, request: HttpRequest):
        forms = CommentForm(self.request.GET)
        return render(request, 'product/detail_product.html', context={'form': forms})

    def post(self, request: HttpRequest):
        forms = CommentForm(self.request.POST)
        if forms.is_valid():
            text = forms.cleaned_data.get('text')

        return render(request, 'product/detail_product.html', context={'form': forms})
