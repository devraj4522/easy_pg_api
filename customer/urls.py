from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("hostel/", views.HostelView.as_view(), name="hostel"),
    path("review/", views.CommentView.as_view(), name="review"),
    path("search-hostel/", views.FilterHostelView.as_view(), name="hostel"),
]
