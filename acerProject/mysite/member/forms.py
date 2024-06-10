from django import forms
from .models import Member
import re, hashlib

class RegisterForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(widget=forms.PasswordInput(), label="password")
    email = forms.CharField(widget=forms.EmailInput(), label="email")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Member.objects.filter(username = username)

        if dbuser:
            return False
        else:
            return username

    def clean_password(self):

        password = self.cleaned_data.get("password")
        check_digit = re.compile(r"(\d+)")
        check_letters  = re.compile(r"(\D+)")
        check_whitespace  = re.compile(r"(\s+)")
        check_special  = re.compile(r"(\W+)")
        check_len = len(password)

        if check_len > 7 and check_len < 13:
            if check_whitespace.search(password):

                return ("should not include white space", "False")

            else:

                if check_digit.search(password) and check_letters.search(password):

                    return (hashlib.sha256(bytes(password, encoding="ascii")).hexdigest(), "True")

                else:

                    return ("should include at least one digit 、 letter and special character", "False")
        else:

            return ("invalid length", "False")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        dbemail = Member.objects.filter(email = email)

        if dbemail:
            return False
        else:
            return email


class LoginForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    password = forms.CharField(widget=forms.PasswordInput(), label="password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Member.objects.filter(username = username)

        if dbuser:
            return username
        else:
            return "username '%s' doesn't existed!" % username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = hashlib.sha256(bytes(self.cleaned_data.get("password"), encoding="ascii")).hexdigest()
        dbpassowrd = Member.objects.get(username = username)

        if password == dbpassowrd.password:
            return True
        else:
            return "There's error in your password!"

class ResetInfoForm(forms.Form):

    username = forms.CharField(max_length=50, label="username")
    email = forms.CharField(widget=forms.EmailInput(), label="email")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Member.objects.filter(username = username)

        if dbuser:
            return username
        else:
            return False

    def clean_email(self):
        email = self.cleaned_data.get("email")
        dbemail = Member.objects.filter(email = email)

        if dbemail:
            return email
        else:
            return False


class ResetForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(), label="password")
    comfirm_password = forms.CharField(widget=forms.PasswordInput(), label="password")

    def clean_comfirm_password(self):

        password = self.cleaned_data.get("password")
        comfirm_password = self.cleaned_data.get("comfirm_password")

        if password[0] != hashlib.sha256(bytes(comfirm_password, encoding="ascii")).hexdigest():

            return True

        else:

            return False

    def clean_password(self):

        password = self.cleaned_data.get("password")
        check_digit = re.compile(r"(\d+)")
        check_letters  = re.compile(r"(\D+)")
        check_whitespace  = re.compile(r"(\s+)")
        check_special  = re.compile(r"(\W+)")
        check_len = len(password)

        if check_len > 7 and check_len < 13:
            if check_whitespace.search(password):

                return ("should not include white space", True)

            else:

                if check_digit.search(password) and check_letters.search(password) and check_special.search(password):

                    return (hashlib.sha256(bytes(password, encoding="ascii")).hexdigest(), False)

                else:

                    return ("should include at least one digit 、 letter and special character", True)
        else:

            return ("invalid length", True)

