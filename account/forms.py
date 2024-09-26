from django.core.exceptions import ValidationError
from django import forms

from account.models import User, Profile


class RegistrationForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=254,
        label="ایمیل یا شماره تلفن خود را وارد کنید",
        )

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier'].strip()
        if identifier.isdigit():
            if User.objects.filter(profile__phone_number__iexact=identifier).exists():
                raise ValidationError("کاربری با این شماره قبلا ثبت نام کرده است.")
        elif "@gmail.com" in identifier:
            if User.objects.filter(email=identifier).exists():
                raise ValidationError(" کاربری با این ایمیل قبلا ثبت نام کرده است.")
        else:
            raise ValidationError("ایمیل یا شماره تلفن معتبر وارد کنید.")
        return identifier


class RegistrationLoginForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=254,
        label='ایمیل یا شماره تلفن خود را وارد کنید',
        help_text="لطفاً ایمیل یا شماره تلفن خود را به صورت معتبر وارد کنید."
    )
    def clean_identifier(self):
        identifier = self.cleaned_data['identifier'].strip()
        if identifier.isdigit():  # اگر شماره موبایل باشد
            if User.objects.filter(profile__phone_number__iexact=identifier).exists():
                raise ValidationError("کاربری با این شماره قبلا ثبت نام کرده است.")

        elif "@" in identifier:  # اگر ایمیل باشد
            if User.objects.filter(email__iexact=identifier).exists():
                raise ValidationError("کاربری با این ایمیل قبلا ثبت نام کرده است.")

        else:
            raise ValidationError("ایمیل یا شماره تلفن معتبر وارد کنید.")

        return identifier


# فرض کنید شما یک مدل پروفایل دارید که شماره تلفن را ذخیره می‌کند


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="کد تأیید")
