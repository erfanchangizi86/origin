from django.core.exceptions import ValidationError
from django import forms

from account.models import User, Profile

error = {
    'max_length': 'طول مجاز 6 رقم است',
}


class RegistrationForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=254,
        label="ایمیل یا شماره تلفن خود را وارد کنید",
    )

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
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
    otp = forms.CharField(max_length=6, min_length=6, label="کد تأیید", error_messages=error)

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        prof = Profile.objects.filter(otp__iexact=otp).first()
        if prof is None:
            raise ValidationError("کد اشتباه است")
        return otp

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        if identifier.isdigit():  # اگر شماره موبایل باشد
            user = User.objects.filter(profile__phone_number__iexact=identifier).exists()
            if not user:
                raise ValidationError("کاربری با این شماره وجود ندارد.")

        elif "@" in identifier:  # اگر ایمیل باشد
            if User.objects.filter(email__iexact=identifier).exists():
                raise ValidationError("کاربری با این ایمیل وجود ندارد.")

        else:
            raise ValidationError("ایمیل یا شماره تلفن معتبر وارد کنید.")

        return identifier


# فرض کنید شما یک مدل پروفایل دارید که شماره تلفن را ذخیره می‌کند


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, label="کد تأیید", error_messages=error)

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        prof = Profile.objects.filter(otp__iexact=otp).first()
        if prof is None:
            raise ValidationError("کد اشتباه است")
        return otp
