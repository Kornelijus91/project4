
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("follow", views.follow, name="follow"),
    path("isfollowing", views.isfollowing, name="isfollowing"),
    path("following", views.following, name="following"),
    path("editpost", views.editpost, name="editpost"),
    path("isliked", views.isliked, name="isliked"),
    path("like", views.like, name="like"),
    path("getlikecount", views.getlikecount, name="getlikecount"),
    path("updatefollowcount", views.updatefollowcount, name="updatefollowcount"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
