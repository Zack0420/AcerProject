from django import forms
from .models import Member
import re, hashlib

class RegisterForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(max_length=256, label="password")
    confirmpw = forms.CharField(max_length=256, label="confirm_pd")
    email = forms.CharField(max_length = 50, label="email")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Member.objects.filter(username = username)

        if dbuser:
            return (True, )
        else:
            return (False, username)

    def clean_password(self):

        password = self.cleaned_data.get("password")
        hashed_pw = hashlib.sha256(bytes(password, encoding="ascii")).hexdigest()
        return hashed_pw

    def clean_confirmpw(self):

        confirmpw = self.cleaned_data.get("confirmpw")
        hashed_pw = hashlib.sha256(bytes(confirmpw, encoding="ascii")).hexdigest()
        password = self.cleaned_data.get("password")

        if hashed_pw != password:
            return True
        else:
            return False

    def clean_email(self):
        email = self.cleaned_data.get("email")
        dbemail = Member.objects.filter(email = email)

        if dbemail:
            return (True, )
        else:
            return (False, email)

class LoginForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(max_length=256, label="password")

    def clean_username(self):

        username = self.cleaned_data.get("username")
        user = Member.objects.filter(username = username)
        if user:
            return (False, username)
        else:
            return (True, )

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = bytes(self.cleaned_data.get("password"), encoding="ascii")
        hashed_password = hashlib.sha256(password).hexdigest()
        if username[0] != True:
            user = Member.objects.get(username = username[1])
            if hashed_password == user.password:
                return (False, )
            else:
                return (True, )
        else:
            return (True, )

class ResetInfoForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    email = forms.CharField(max_length=50, label="email")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Member.objects.filter(username = username)

        if dbuser:
            return (False,username)
        else:
            return (True, )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        dbemail = Member.objects.filter(email = email)

        if dbemail:
            return (False, email)
        else:
            return (True, )


class ResetForm(forms.Form):

    password = forms.CharField(max_length=256, label="password")
    confirmpw = forms.CharField(max_length=256, label="confirmpw")
    username = forms.CharField(widget=forms.HiddenInput,max_length=50, label="username")

    def clean_password(self):

        password = self.cleaned_data.get("password")
        hashed_pw = hashlib.sha256(bytes(password, encoding="ascii")).hexdigest()
        return hashed_pw

    def clean_confirmpw(self):

        confirmpw = self.cleaned_data.get("confirmpw")
        hashed_pw = hashlib.sha256(bytes(confirmpw, encoding="ascii")).hexdigest()
        password = self.cleaned_data.get("password")

        if hashed_pw != password:
            return True
        else:
            return False

    def clean_username(self):

        username = self.cleaned_data.get("username")

        return username