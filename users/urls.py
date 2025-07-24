from django.urls import path
from . import views

app_name = "users" # for namespacing in templates or reverse()
urlpatterns = [
    # Auth
    path('register/',views.register_view,name="register")
]
