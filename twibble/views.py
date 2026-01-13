from django.shortcuts import get_object_or_404, render, redirect
from users.models import TwibbleUser
from tweets.models import Tweet
from django.db import models


def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        following_users = current_user.following.all()
        tweets = Tweet.objects.filter(user__in=following_users).order_by("-created_at")
    else:
        following_users = []
        tweets = Tweet.objects.all().order_by("-created_at")[:10]
    return render(
        request,
        "base.html",
        {
            "current_user": current_user,
            "tweets": tweets,
            "following_users": following_users,
        },
    )


def search_view(request):
    query = request.GET.get("q", "").strip()
    user_results = []
    tweet_results = []

    if query:  # only search if query is not empty
        user_results = TwibbleUser.objects.filter(
            models.Q(username__icontains=query)
            | models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(bio__icontains=query)
        )

        # search tweets by text            raise
        tweet_results = Tweet.objects.filter(text__icontains=query)
    context = {
        "query": query,
        "user_results": user_results,
        "tweet_results": tweet_results,
    }
    return render(request, "search_results.html", context)
