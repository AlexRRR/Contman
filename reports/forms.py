from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class SearchForm(forms.Form):
    sdate = forms.DateField(input_formats=['%Y-%m-%d'],required=True,widget=forms.DateInput(attrs={'class': 'dateentry',}))
    edate = forms.DateField(input_formats=['%Y-%m-%d'],required=True,widget=forms.DateInput(attrs={'class': 'dateentry',}))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        sdate = cleaned_data.get("sdate")
        edate = cleaned_data.get("edate")
        if not self.errors:
            if not edate > sdate:
                raise forms.ValidationError("Start date must be earlier than end date")
        return cleaned_data
