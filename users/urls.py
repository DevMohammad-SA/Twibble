from django.urls import path
from . import views

app_name = "users"  # for namespacing in templates or reverse()
urlpatterns = [
    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/<int:user_id>", views.profile_view, name="profile"),
]
