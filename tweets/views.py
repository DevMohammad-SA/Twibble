from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string

from users.models import TwibbleUser
from .models import Tweet
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def post_view(request):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()

        # Check if the post is empty
        if not text:
            return HttpResponse("<p class='text-danger'>Tweet cannot be empty.</p>")

        # Post length Check
        if len(text) > 300:
            return HttpResponse(
                "<p class='text-danger'>Tweet is too long (max 300 characters).</p>"
            )
        tweet = Tweet.objects.create(user=request.user, text=text)

        if request.headers.get("HX-Request"):
            # We send only the HTML fragment for the new tweet if the request is from HTMX,
            # allowing for a partial page update instead of a full redirect.
            html = render_to_string(
                "tweets/_tweet_card.html", {"tweet": tweet}, request=request
            )
            return HttpResponse(html)
        return redirect("home")
    return redirect("home")


@login_required()
def edit_tweet_view(request, tweet_id):
    print("EDIT VIEW CALLED")
    tweet = get_object_or_404(Tweet, id=tweet_id)

    referer = request.META.get("HTTP_REFERER")
    # only tweet author can change the tweet
    if tweet.user != request.user:
        if request.headers.get("HX-Request"):
            return HttpResponse("Not Allowed", status=403)
        return redirect("home")

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            return HttpResponse("<p class='text-danger'>Tweet cannot be empty.</p>")

        # Post length Check
        if len(text) > 300:
            return HttpResponse(
                "<p class='text-danger'>Tweet is too long (max 300 characters).</p>"
            )
        tweet.text = text
        tweet.is_edited = True
        tweet.save()

        if request.headers.get("HX-Request"):
            html = render_to_string(
                "tweets/_tweet_card.html", {"tweet": tweet}, request=request
            )
            return HttpResponse(html)

        if referer:
            return HttpResponseRedirect(referer)
        return redirect("home")
    # GET request
    if request.headers.get("HX-Request"):
        return render(request, "tweets/_edit_form.html", {"tweet": tweet})
    if referer:
        return HttpResponseRedirect(referer)
    return redirect("home")


@login_required()
def like_view(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    # Toggle
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    return render(request, "tweets/_like_button.html", {"tweet": tweet})


@login_required()
def pin_post_view(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    print("pin_post_view triggered")

    # only the owner can pin his post
    if request.user == tweet.user:
        if tweet.is_pinned:
            tweet.is_pinned = False
            tweet.save()
        else:
            # if the post is not pinned, first unpin the previous pinned post if available
            Tweet.objects.filter(user=request.user, is_pinned=True).update(
                is_pinned=False
            )
            # and then pin the new one
            tweet.is_pinned = True
            tweet.save()

    return redirect(request.META.get("HTTP_REFERER", "profile"))


@login_required()
def delete_post_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    # Check if the logged in user is the tweet owner
    if tweet.user != request.user:
        raise PermissionDenied("You are not allowed to delete this tweet.")
    tweet.delete()

    # redirect to the referer (previous page) if available
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect("home")
