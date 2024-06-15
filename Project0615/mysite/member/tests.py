from django.test import TestCase
from .models import Member

# Create your tests here.
def change_data(request, username, pd):

    member = Member.objects.get(username = username)
    member.password = pd
    member.save()