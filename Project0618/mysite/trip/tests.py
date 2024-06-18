from django.test import TestCase
from .models import User_save
import datetime

# Create your tests here.
def period_changed(reqeust):

    today = '2024/6/18'
    date = '2024/6/19'

    td = datetime.datetime.strptime(today, "%Y/%m/%d")
    dt =  datetime.datetime.strptime(date, "%Y/%m/%d")

    after_a_week = td + datetime.timedelta(days = 7)


    
    print(after_a_week)
    print(dt<after_a_week)
    print(td<dt)
    
    