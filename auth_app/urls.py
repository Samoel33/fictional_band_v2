from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from . import views

app_name = "auth_app"
urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
]
