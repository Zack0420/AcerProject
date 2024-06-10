from django.contrib import admin
from django.urls import path, include
from member import views
from django.urls import re_path as url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^home/', views.home, name = "home"),
    url(r'^registerForm/(?P<message>.*)/(?P<alert>.*)/', views.registerForm, name = "registerForm"),
    url(r'^register/', views.register, name = "register"),
    url(r'^loginForm/', TemplateView.as_view(template_name='login.html'), name = "loginForm"),
    url(r'^login/', views.login, name = "login"),
    url(r'^logout/', views.logout, name = "logout"),
    url(r'^profile/', views.profile, name = "profile"),
    url(r'^verifyEmail/', views.verifyEmail, name = "verifyEmail"),
    url(r'^verify/(?P<username>.*)/', views.verify, name = "verify"),
    url(r'^resetInfoForm/(?P<message>.*)/(?P<alert>.*)/', views.resetInfoForm, name = "resetInfoForm"),
    url(r'^resetInfo/', views.resetInfo, name = "resetInfo"),
    url(r'^resetEmail/', views.sendResetEmail, name = "sendResetEmail"),
    url(r'^resetForm/(?P<message>.*)/(?P<alert>.*)/', views.resetForm, name = "resetForm"),
    url(r'^reset/', views.reset, name = "reset"),
]