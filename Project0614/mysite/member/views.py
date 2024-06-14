from django.shortcuts import render, redirect
from .models import Member
from member.forms import RegisterForm, LoginForm, ResetInfoForm, ResetForm, ProfileForm
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

def home(request):

    if "username" not in request.COOKIES.keys():

        return render(request, "home.html")

    else:

        return render(request, "index.html", {"username": request.COOKIES["username"]})

def signupForm(request):

    if "usermsg" not in request.COOKIES.keys():

        usermsg = False
        cfpmsg = False
        emailmsg = False

        response = render(request, "signup.html", {"usermsg": usermsg, "cfpmsg":cfpmsg, "emailmsg":emailmsg})
        return response
    else:

        usermsg = request.COOKIES['usermsg']
        cfpmsg = request.COOKIES['cfpmsg']
        emailmsg = request.COOKIES['emailmsg']

        response = render(request, "signup.html", {"usermsg": usermsg, "cfpmsg":cfpmsg, "emailmsg":emailmsg})

        response.delete_cookie('usermsg')
        response.delete_cookie('cfpmsg')
        response.delete_cookie('emailmsg')

        return response

def signup(request):

    if request.method == "POST":
        signupForm = RegisterForm(request.POST)

        resignup_res = redirect('signupForm')

        if signupForm.is_valid():
            username = signupForm.cleaned_data["username"]
            password = signupForm.cleaned_data["password"]
            confirmpw = signupForm.cleaned_data["confirmpw"]
            email = signupForm.cleaned_data["email"]

            if username[0]:

                resignup_res.set_cookie("usermsg", username[0])
                username = None

            else:

                resignup_res.set_cookie("usermsg", username[0])
                username = username[1]


            resignup_res.set_cookie("cfpmsg", confirmpw)

            if email[0]:

                resignup_res.set_cookie("emailmsg", email[0])
                email = None

            else:

                resignup_res.set_cookie("emailmsg", email[0])
                email = email[1]

            if username != None and confirmpw == False and email != None:

                member = Member(username = username, password = password, email = email, verification = False)
                member.save()

                verifyEmail = redirect('verifyEmail')
                verifyEmail.set_cookie('username', username)
                verifyEmail.set_cookie('email', email)
                return verifyEmail

            else:
                return resignup_res

        else:

            signupForm = RegisterForm()
            return redirect('home')

    return redirect('home')

def loginForm(request):
    if "usermsg" not in request.COOKIES.keys():
        usermsg = False
        pwdmsg = False
        response = render(request, "login.html", {"usermsg": usermsg, "pwdmsg":pwdmsg})
        return response

    else:
        usermsg = request.COOKIES['usermsg']
        pwdmsg = request.COOKIES['pwdmsg']

        response = render(request, "login.html", {"usermsg": usermsg, "pwdmsg":pwdmsg})

        response.delete_cookie('usermsg')
        response.delete_cookie('pwdmsg')

        return response

def login(request):

    if request.method == "POST":

        loginForm = LoginForm(request.POST)

        relogin_res = redirect('loginForm')
        logined_res = redirect('home')

        if loginForm.is_valid():

            username = loginForm.cleaned_data["username"]
            if username[0] == False:
                password = loginForm.cleaned_data["password"]
                if password[0] == False:

                    logined_res.set_cookie('username', username[1])

                    return logined_res
                else:

                    relogin_res.set_cookie('usermsg', username[0])
                    relogin_res.set_cookie('pwdmsg',  True)

                    return relogin_res
            else:

                relogin_res.set_cookie('usermsg', username[0])
                relogin_res.set_cookie('pwdmsg',  False)

                return relogin_res

        else:

            loginForm = LoginForm()
            return redirect('home')

    return redirect('home')

def profile(request):

    if "username" in request.COOKIES.keys():

        username = request.COOKIES['username']
        email = Member.objects.get(username = username).email
        return render(request, "profileinfo.html", {"username":username, "email":email})

    else:

        return redirect("home")

def logout(request):

    keys = request.COOKIES.keys()
    response = redirect('home')
    for k in list(keys):
        response.delete_cookie(k)

    return response

def verifyEmail(request):

    if "email" in request.COOKIES and "username" in request.COOKIES:

        emailto = request.COOKIES["email"]
        username = request.COOKIES["username"]

        subject, from_email, to = 'Welcome to app', 'han1010227@gmail.com', emailto
        text_content = 'Verify your email!'
        html_content = '<a href = "http://127.0.0.1:8000/member/change_verifiction_status/%s">Pleask click here to verify your email!</p>'%username
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response = redirect('loginForm')

        response.delete_cookie("email")
        response.delete_cookie("username")

        return response

    else:

        return redirect('home')

def change_verifiction_status(request, username):

    member = Member.objects.get(username = username)
    member.verification = True
    member.save()
    return HttpResponse("驗證完成請關閉此分頁")

def resetInfoForm(request):

    if "usermsg" not in request.COOKIES.keys():

        usermsg = False
        emailmsg = False

        response = render(request, "resetInfo.html", {"usermsg": usermsg, "emailmsg":emailmsg})
        return response
    else:

        usermsg = request.COOKIES['usermsg']
        emailmsg = request.COOKIES['emailmsg']

        response = render(request, "resetInfo.html", {"usermsg": usermsg, "emailmsg":emailmsg})

        response.delete_cookie('usermsg')
        response.delete_cookie('emailmsg')

        return response

def resetInfo(request):

    if request.method == "POST":

        resetInfoForm = ResetInfoForm(request.POST)

        if resetInfoForm.is_valid():

            username = resetInfoForm.cleaned_data['username']
            reresetInfo = redirect("resetInfoForm")
            sendResetEmail = redirect("resetEmail")
            if username[0] == False:

                sendResetEmail.set_cookie('username', username[1])
                email = resetInfoForm.cleaned_data['email']

                if email[0] == False:

                    sendResetEmail.set_cookie('email', email[1])

                    return sendResetEmail

                else:

                    reresetInfo.set_cookie('usermsg', False)
                    reresetInfo.set_cookie('emailmsg', email[0])

                    return reresetInfo
            else:

                reresetInfo.set_cookie('usermsg', username[0])
                reresetInfo.set_cookie('emailmsg', False)

                return reresetInfo



    else:

        return redirect("home")

def sendResetEmail(request):

    if "email" in request.COOKIES and "username" in request.COOKIES:

        emailto = request.COOKIES["email"]
        username = request.COOKIES["username"]

        subject, from_email, to = 'Welcome to app', 'han1010227@gmail.com', emailto
        text_content = 'Rest your password!'
        html_content = '<a href = "http://127.0.0.1:8000/member/resetForm/%s">Pleask click here to reset your password!</p>'%username
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response = redirect('home')

        response.delete_cookie("email")
        response.delete_cookie("username")

        return response

    else:

        return redirect('home')

def resetForm(request, username):

    if "cfpmsg" not in request.COOKIES.keys():

        cfpmsg = False

        response = render(request, "resetForm.html", {"cfpmsg":cfpmsg, "username":username})
        return response
    else:

        cfpmsg = request.COOKIES['cfpmsg']

        response = render(request, "resetForm.html", {"cfpmsg":cfpmsg, "username":username})
        response.delete_cookie('cfpmsg')

        return response

def reset(request):

    if request.method == "POST":

        resetForm = ResetForm(request.POST)
        if resetForm.is_valid():

            password = resetForm.cleaned_data["password"]
            confirmpw = resetForm.cleaned_data["confirmpw"]
            username = resetForm.cleaned_data['username']
            rereset_res = redirect('resetForm', username)

            if confirmpw:

                rereset_res.set_cookie("cfpmsg", confirmpw)

                return rereset_res

            else:

                member = Member.objects.get(username=username)
                member.password = password
                member.save()

                response = redirect("loginForm")

                response.delete_cookie('username')

                return response

        else:

            resetForm = ResetForm()

    return redirect('logout')

def saveChanged(request):

    if request.method == "POST":

        profileForm = ProfileForm(request.POST)

        if profileForm.is_valid():

            username = request.COOKIES['username']
            email = profileForm.cleaned_data['email']

            member = Member.objects.get(username = username)

            member.email = email

            member.save()

            return redirect('profile')

        else:

            profileForm = ProfileForm()

    else:

        return redirect('profile')

def deleteAccount(request):

    username = request.COOKIES['username']
    member = Member.objects.get(username = username)
    Member.objects.get(id = member.id).delete()

    return redirect('logout')