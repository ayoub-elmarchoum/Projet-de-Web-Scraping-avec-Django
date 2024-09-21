from django.shortcuts import render
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home_page"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.regis, name="register"),
    path('scrape/', views.scrape_v2, name="scrape"),
]