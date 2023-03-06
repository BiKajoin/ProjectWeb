from django import forms

class DateFilterForm(forms.Form):
    year = forms.IntegerField(required=False)
    month = forms.IntegerField(required=False)
    day = forms.IntegerField(required=False)
