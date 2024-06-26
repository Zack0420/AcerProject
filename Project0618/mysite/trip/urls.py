"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from trip import views, tests
from django.urls import re_path as url


urlpatterns = [
    path('test/', tests.period_changed),
    path('area/', views.area,name='area'),
    path('search_results/', views.search_results, name='search_results'),
    path('add_to_itinerary/', views.add_to_itinerary, name='add_to_itinerary'),
    path('delete_from_itinerary/', views.delete_from_itinerary, name='delete_from_itinerary'),
    path('personal_page/', views.personal_page, name='personal_page'),
    url(r'^user_save_delete/', views.user_save_delete, name = "user_save_delete"),
    url(r'^sendemail/', views.sendemail, name = "sendemail"),
    url(r'^period_change/', views.period_changed, name = "period_change"),

]



