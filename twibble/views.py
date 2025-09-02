from django.shortcuts import get_object_or_404, render, redirect
from users.models import TwibbleUser
from tweets.models import Tweet
def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        following_users = current_user.following.all()
        tweets = Tweet.objects.filter(user__in=following_users).order_by('-created_at')
    else:
        following_users = []
        tweets = Tweet.objects.all().order_by('-created_at')[:10]
    return render(request, "base.html",{
        "current_user":current_user,
        "tweets":tweets,
        "following_users":following_users
    })
