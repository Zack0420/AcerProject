# forms.py
from django import forms

class PriceRangeForm(forms.Form):
    price1 = forms.IntegerField(label='最低價格', min_value=10, max_value=100000, )#required=False
    price2 = forms.IntegerField(label='最高價格', min_value=100, max_value=1000000)#required=False
    # day = forms.IntegerField(label='天數',min_value=1, max_value=100)

class PersonalPageForm(forms.Form):
    username = forms.CharField(max_length=50, label="username")
    title = forms.CharField(max_length=100, label="title")
    company = forms.CharField(max_length=256, label="company")
    date = forms.CharField(max_length = 50, label="date")

    def clean_username(self):

        username = self.cleaned_data.get("username")

        return username
    def clean_title(self):

        title = self.cleaned_data.get("title")
        return title+"\n"
    
    def clean_company(self):

        company = self.cleaned_data.get("company")

        return company
    def clean_date(self):

        date = self.cleaned_data.get("date")

        return date
    
class PeriodForm(forms.Form):

    period = forms.CharField(max_length=50, label="period")
    

    def clean_peroid(self):

        period = self.cleaned_data.get('period')

        return period