
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.post, name="post"),
    path("likes", views.like_post, name= "likes"),
    path('profile/<str:userq>', views.profile, name="profile"),
    path("follow", views.follow, name = "follow"),
    path("following",views.following,name="following"),
    path("edit",views.edit, name = "edit")

]
