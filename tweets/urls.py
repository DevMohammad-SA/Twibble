from django.urls import path

from . import views

app_name = "tweets"

urlpatterns = [
    path("<int:pk>/", views.tweet_detail_view, name="detail"),
    path("post/", views.post_view, name="post"),
    path("<int:pk>/like/", views.like_view, name="like"),
    path("<int:pk>/bookmark/", views.bookmark_toggle_view, name="bookmark_toggle"),
    path("bookmarks/", views.bookmarks_list_view, name="bookmarks_list"),
    path("delete/<int:tweet_id>/", views.delete_post_view, name="delete"),
    path("pin/<int:pk>/", views.pin_post_view, name="pin"),
    path("edit/<int:tweet_id>", views.edit_tweet_view, name="edit"),
    path("<int:pk>/reply/", views.reply_view, name="reply"),
    path("tag/<str:slug>/", views.tag_view, name="tag"),
]
