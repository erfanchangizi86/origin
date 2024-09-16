from django import forms

error = {
    'required': 'این فیلد اجباری است.',
    'max_length': 'حداکثر طول مجاز برای این فیلد 500 کاراکتر است.',
}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=120, error_messages=error,
                             widget=forms.TextInput(
                                 attrs={ 'placeholder': "جستجو ...",'autocomplete':"off"})
                             )


class CommentForm(forms.Form):
    pass