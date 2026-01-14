from django.urls import path
from . import views

app_name = "tweets"

urlpatterns = [
    path("post/", views.post_view, name="post"),
    path("<int:pk>/like/", views.like_view, name="like"),
    path("delete/<int:tweet_id>/", views.delete_post_view, name="delete"),
    path("pin/<int:pk>/", views.pin_post_view, name="pin"),
]
