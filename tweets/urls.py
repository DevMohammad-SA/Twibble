from django.urls import path
from . import views

app_name = "tweets"

urlpatterns = [
    path("post/",views.post_view,name="post"),
]
