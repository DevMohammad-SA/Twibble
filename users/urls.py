from django.urls import path
from . import views

app_name = "users"  # for namespacing in templates or reverse()
urlpatterns = [
    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("@<str:username>/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("follow/<str:username>/",views.follow_view, name="follow"),
    path("unfollow/<str:username>/",views.unfollow_view,name="unfollow"),
    path("@<str:username>/followers",views.followers_list_view,name="followers_list"),
    path("@<str:username>/followings",views.following_list_view,name="following_list")
]
