from django.core.exceptions import ValidationError
from django import forms

from account.models import User, Profile


class RegistrationForm(forms.Form):
    identifier = forms.CharField(max_length=254, label="ایمیل یا شماره تلفن خود را وارد کنید",widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'erfan@gmail.com'}))
    password = forms.CharField(label='رمز عبور' , widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                                    'placeholder': 'حداقل 5 کارکتر باشد '}))
    confirm_password = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'حداقل 5 کارکتر باشد '}))

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        # if identifier.isdigit():
        #     if User.objects.filter(phone_number__iexact=identifier).exists():
        #         raise ValidationError("کاربری با این شماره قبلا ثبت نام کرده است.")
        # if "@gmail.com" in identifier:
        if User.objects.filter(email=identifier).exists():
            raise ValidationError(" کاربری با این ایمیل قبلا ثبت نام کرده است.")
        # else:
        #     raise ValidationError("ایمیل یا شماره تلفن معتبر وارد کنید.")
        return identifier

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']
        if len(password) < 5 and len(confirm_password) < 5:
            raise ValidationError('رمز  عبور حداقل باید 5 کاراکتر باشد.')
        if password != confirm_password:
            raise ValidationError('تکرار رمز عبور مطابقت ندارد.')
        if confirm_password[0].isdigit() and password[0].isdigit():
            raise ValidationError('رمز عبور نباید با عدد شروع شود.')
        return confirm_password


class RegistrationLoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),max_length=254,label='ایمیل خود را وارد کنید', help_text="ایمیل یا شماره تلفن خود را وارد کنید")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                    }),label='رمز عبور خود را وارد کنید', help_text="رمز عبور خود را وارد کنید")

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        # if identifier.isdigit():
        #     if not User.objects.filter(phone_number=identifier).exists():
        #         raise ValidationError("هیچ کاربری با این شماره تلفن یافت نشد.")
        # if "@gmail.com" in identifier:
        if not User.objects.filter(email=identifier).exists():
            raise ValidationError("هیچ کاربری با این ایمیل یافت نشد.")
        # else:
        #     raise ValidationError("ایمیل  معتبر وارد کنید.")
        return identifier

# فرض کنید شما یک مدل پروفایل دارید که شماره تلفن را ذخیره می‌کند
