from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string

from users.models import TwibbleUser
from .models import Tweet
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required()
def post_view(request):
    if request.method == "POST":
        text = request.POST.get("text","").strip()

        if not text:
            return HttpResponse("<p class='text-danger'>Tweet cannot be empty.</p>")

        tweet = Tweet.objects.create(user=request.user,text=text)

        if request.headers.get("HX-Request"):
            html = render_to_string("tweets/_tweet_card.html",{"tweet":tweet})
            return HttpResponse(html)
        return redirect("home")
    return redirect("home")

@login_required()
def like_view(request,pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    # Toggle
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    return render(request,"tweets/_like_button.html",{"tweet":tweet})
