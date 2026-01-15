from django.shortcuts import get_object_or_404, render, redirect
from users.models import TwibbleUser
from tweets.models import Tweet
from django.db import models
from django.core.paginator import Paginator


def home(request):
    current_user = request.user
    feed_type = request.GET.get("feed", "for-you")
    following_users = []
    page_number = request.GET.get("page")
    if current_user.is_authenticated:
        following_users = current_user.following.all()

    if feed_type == "following" and current_user.is_authenticated:
        tweets_queryset = Tweet.objects.filter(
            models.Q(user__in=following_users) | models.Q(user=current_user)
        ).order_by("-created_at")
    else:
        tweets_queryset = Tweet.objects.all().order_by("-created_at")

    paginator = Paginator(tweets_queryset, 5)  # 5 tweets per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "base.html",
        {
            "current_user": current_user,
            "tweets": page_obj,  # Send the page_obj instead of the queryset
            "feed_type": feed_type,
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
