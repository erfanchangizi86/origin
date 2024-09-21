from django import forms

error = {
    'max_length': 'حداکثر طول مجاز برای این فیلد 500 کاراکتر است.',
}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=120, error_messages=error,
                             widget=forms.TextInput(
                                 attrs={ 'placeholder': "جستجو ...",'autocomplete':"off"})
                             )


class CommentForm(forms.Form):
    text = forms.CharField(max_length=120, error_messages=error
                           ,widget=forms.Textarea(attrs={'class':'form-control form-control-sm',
                                                         'placeholder':'دیدگاه شما ...',
                                                         'rows':4}),label='متن نظر')