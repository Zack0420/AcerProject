from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from member.forms import RegisterForm, LoginForm, ResetForm, ResetInfoForm
from django.core.mail import EmailMultiAlternatives
import hashlib
from django.template import loader


# Create your views here.
def home(request):

    if request.session.has_key('username'):
        print(request.session['username'])
        username = request.session['username']

        return render(request, 'index.html', {"username":username})

    else:
        
        return render(request, 'home.html')

        

def registerForm(request, alert = "False", message = "none"):

    return render(request, "signup.html", {"message": message, "alert":alert})

def register(request):

    if request.method == "POST":
        registerForm = RegisterForm(request.POST)

        if registerForm.is_valid():
            username = registerForm.cleaned_data["username"]
            password = registerForm.cleaned_data["password"]
            email = registerForm.cleaned_data["email"]

            if password[1] == "False":

                return redirect('registerForm', message = password[0], alert = "True")

            elif username == False:

                return redirect('registerForm', message = "Username is existed!", alert = "True")

            elif email == False:

                return redirect('registerForm', message = "Email is existed!", alert = "True")


            member = Member(username = username, password = password[0], email = email, verification = False)
            member.save()

            response = redirect('verifyEmail')

            response.set_cookie("email", email)
            response.set_cookie("username", username)

            return response
        else:

            registerForm = RegisterForm()


        return redirect('home')

def login(request):

    if request.method == "POST":
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data["username"]
            password = loginForm.cleaned_data["password"]

            try:

                if password:

                        request.session['username'] = username
                        return redirect('home')
                else:

                        return HttpResponse(password)

            except Exception as e:

                print(e)
                return HttpResponse(username)

        else:

            loginForm = LoginForm()

    return redirect('home')

def logout(request):

    try:
        del request.session['username']
    except:
        print(1)
        pass

    return redirect('home')

def profile(request):

    username = request.session['username']
    email = Member.objects.get(username = username).email

    return render(request, 'profileinfo.html', {'username':username, 'email':email})

def verify(request, username):
    member = Member.objects.get(username = username)
    member.verification = True
    member.save()
    return redirect('home')

def verifyEmail(request):

    if "email" in request.COOKIES and "username" in request.COOKIES:

        emailto = request.COOKIES["email"]
        username = request.COOKIES["username"]

        subject, from_email, to = 'Welcome to app', 'han1010227@gmail.com', emailto
        text_content = 'Verify your email!'
        html_content = '<a href = "http://127.0.0.1:8000/member/verify/%s">Pleask click here to verify your email!</p>'%username
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response = redirect('home')

        response.delete_cookie("email")
        response.delete_cookie("username")

        return response

    else:

        return redirect('home')


def resetInfoForm(request, alert = "False", message = "none"):

    return render(request, "resetInfo.html", {"message": message, "alert":alert})

def resetInfo(request):

    if request.method == "POST":
        resetInfoForm = ResetInfoForm(request.POST)

        if resetInfoForm.is_valid():
            username = resetInfoForm.cleaned_data["username"]
            email = resetInfoForm.cleaned_data["email"]

            if username == False:

                return redirect('resetInfoForm', message = "Username is not existed!", alert = "True")

            elif email == False:

                return redirect('resetInfoForm', message = "Email is not existed!", alert = "True")


            response = redirect('sendResetEmail')

            response.set_cookie("email", email)
            response.set_cookie("username", username)

            return response
        else:

            resetInfoForm = ResetInfoForm()


        return redirect('home')

def sendResetEmail(request):

    if "email" in request.COOKIES and "username" in request.COOKIES:
        username = request.COOKIES["username"]
        emailto = request.COOKIES["email"]
        request.session['username'] = username
        subject, from_email, to = 'Reset password', 'han1010227@gmail.com', emailto
        text_content = 'Reset your password!'
        str_url = redirect(resetForm, "none", "False")
        html_content = '<a href = "http://127.0.0.1:8000'+ str_url.url +'">Pleask click here to reset your password!</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response = redirect('home')

        response.delete_cookie("email")
        response.delete_cookie("username")

        return response

    else:

        return redirect('home')

def resetForm(request, alert = "False", message = "none"):
    return render(request, "resetForm.html", {"message": message, "alert":alert})

def reset(request):

    if request.method == "POST":
        resetForm = ResetForm(request.POST)

        if resetForm.is_valid():
            comfirm_password = resetForm.cleaned_data["comfirm_password"]
            password = resetForm.cleaned_data["password"]
            username = request.session['username']

            if password[1]:

                return redirect('resetForm', message = password[0], alert = "True")

            elif comfirm_password:

                return redirect('resetForm', message = "Comfirm password is wrong!", alert = "True")

            member = Member.objects.get(username = username)
            member.password = password[0]
            member.save()

            try:

                del request.session['username']

            except:

                pass

            response = redirect('home')
            return response
        else:

            resetForm = ResetForm()


        return redirect('home')