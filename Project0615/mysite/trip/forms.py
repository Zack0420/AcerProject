# forms.py
from django import forms

class PriceRangeForm(forms.Form):
    price1 = forms.IntegerField(label='最低價格', min_value=10, max_value=100000, )#required=False
    price2 = forms.IntegerField(label='最高價格', min_value=100, max_value=1000000)#required=False
    # day = forms.IntegerField(label='天數',min_value=1, max_value=100)

# class submitForm(forms.ModelForm):
#     class Meta:
#         model = User_save
#         fields = ['travel_company','area','title', 'price',
#                   'date','departure_city', 'duration', 'remaining_quota',
#                   'tour_schedule','url']


