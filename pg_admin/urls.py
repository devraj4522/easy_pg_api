from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="verify_and_login"),
]
