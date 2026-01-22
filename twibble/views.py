from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count
from django.shortcuts import render

from tweets.models import Tweet
from users.models import TwibbleUser


def home(request):
    current_user = request.user
    feed_type = request.GET.get("feed", "for-you")
    following_users = []
    page_number = request.GET.get("page")
    if current_user.is_authenticated:
        following_users = current_user.following.all()

    if feed_type == "following" and current_user.is_authenticated:
        tweets_queryset = Tweet.objects.filter(
            models.Q(user__in=following_users) | models.Q(user=current_user),
            is_reply=False,  # Hide replies in Following feeds, so it's showing only tweets
        ).order_by("-created_at")
    else:
        # For You feed: Most liked and friends of friends:
        if current_user.is_authenticated:
            my_followings = current_user.following.all()
            friends_of_friends = (
                TwibbleUser.objects.filter(followers__in=my_followings)
                .exclude(id=current_user.id)
                .exclude(id__in=my_followings)
            )

            # get tweets from friends of friends OR any populoar tweets
            tweets_queryset = (
                Tweet.objects.annotate(like_count=Count("likes"))
                .filter(
                    models.Q(user__in=friends_of_friends)  # friends of friends
                    | models.Q(like_count__gte=1)  # or has at least 1 like
                )
                .order_by("-like_count", "-created_at")
            )
        # not logged in, just show most popular tweets
        tweets_queryset = Tweet.objects.annotate(like_count=Count("likes")).order_by(
            "-like_count", "-created_at"
        )

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
            | models.Q(display_name__icontains=query)
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
