from django.contrib import admin
from django.urls import path, include
from member import views
from django.urls import re_path as url
from django.views.generic import TemplateView
from member import tests

urlpatterns = [
    url(r'^home/', views.home, name = "home"),
    url(r'signupForm/', views.signupForm, name = "signupForm"),
    url(r'^signup/', views.signup, name = "signup"),
    url(r'^loginForm/', views.loginForm, name = "loginForm"),
    url(r'^login/', views.login, name = "login"),
    url(r'^profile/', views.profile, name = "profile"),
    url(r'^logout/', views.logout, name = "logout"),
    url(r'^verifyemail/', views.verifyEmail, name = "verifyEmail"),
    url(r'^change_verifiction_status/(?P<username>.*)/', views.change_verifiction_status, name = "change_verifiction_status"),
    url(r'^resetInfoForm/', views.resetInfoForm, name = "resetInfoForm"),
    url(r'^resetInfo/', views.resetInfo, name = "resetInfo"),
    url(r'^resetEmail/', views.sendResetEmail, name = "resetEmail"),
    url(r'^resetForm/(?P<username>.*)/', views.resetForm, name = "resetForm"),
    url(r'^reset/', views.reset, name = "reset"),
    url(r'^saveChanged/', views.saveChanged, name = "savechange"),
    url(r'^deleteaccount/', views.deleteAccount, name = "deleteaccount"),


]
