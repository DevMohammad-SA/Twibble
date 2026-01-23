from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
    TwibbleUserCreationForm,
    TwibbleAuthenticationForm,
    TwibbleUserSettingsForm,
)
from tweets.forms import TweetForm
from .models import TwibbleUser
from tweets.models import Tweet
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.db.models import Case, When, BooleanField

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv

load_dotenv()


# Create your views here
def register_view(request):
    if request.method == "POST":
        form = TwibbleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # generate token and uid
            current_site = get_current_site(request)
            mail_subject = "Activate your Twibble account"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # construct activate link
            protocol = "https" if request.is_secure() else "http"
            activation_link = (
                f"{protocol}://{current_site.domain}/users/activate/{uid}/{token}/"
            )
            message = f"Hi {user.username},\n\nPlease click on the link to confirm your registeration\n{activation_link}"

            # send email
            send_mail(
                mail_subject,
                message,
                os.getenv("EMAIL_HOST_USER"),
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request, "Please check your email to complete the registeration"
            )
            return redirect("users:login")
    else:
        form = TwibbleUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def activate_view(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Thank you for your email confirmation, you can now log in"
        )
        return redirect("users:login")
    else:
        messages.error(request, "Activation link is invalid or expired!")
        return redirect("users:register")


def login_view(request):
    # if user is already logged in, flash message and redirect to users/profile
    if request.user.is_authenticated:
        authentication_form = TwibbleAuthenticationForm(request.POST, data=request.POST)
        user = authentication_form.get_user()
        messages.info(request, "You're already logged in.")
        return redirect("users:profile", username=request.user.username)
    # if user is not logged in
    if request.method == "POST":
        authentication_form = TwibbleAuthenticationForm(request.POST, data=request.POST)
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username} !")
            return redirect("users:profile", username=user.username)
        else:
            messages.warning(request, "Invalid username or password.")
    else:
        authentication_form = TwibbleAuthenticationForm()

    return render(
        request, "users/login.html", {"authentication_form": authentication_form}
    )


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(TwibbleUser, username=username)
    tweets = (
        Tweet.objects.filter(user=profile_user)
        .order_by(
            "-is_pinned",  # pinned tweet first
            "-created_at",  # then the newwest
        )
        .exclude(is_reply=True)
    )
    replies = Tweet.objects.filter(user=profile_user).order_by("-created_at")
    current_user = request.user
    # Check if current_user is already following profile_user
    already_following = profile_user in current_user.following.all()
    form = TweetForm(request.POST)
    context = {
        "profile_user": profile_user,
        "tweets": tweets,
        "current_user": current_user,
        "already_following": already_following,
        "replies": replies,
        "form": form,
    }
    return render(request, "users/profile.html", context)


@login_required
def follow_view(request, username):
    profile_user = get_object_or_404(TwibbleUser, username=username)
    if request.user != profile_user:
        request.user.following.add(profile_user)
    return render(
        request,
        "users/_follow_button.html",
        {"profile_user": profile_user, "current_user": request.user},
    )


@login_required
def unfollow_view(request, username):
    profile_user = get_object_or_404(TwibbleUser, username=username)
    if request.user != profile_user:
        request.user.following.remove(profile_user)
    return render(
        request,
        "users/_follow_button.html",
        {"profile_user": profile_user, "current_user": request.user},
    )


@login_required
def followers_list_view(request, username):
    profile_user = get_object_or_404(TwibbleUser, username=username)
    followers = profile_user.followers.all()
    return render(
        request,
        "users/followers_list.html",
        {
            "profile_user": profile_user,
            "followers": followers,
        },
    )


@login_required
def following_list_view(request, username):
    profile_user = get_object_or_404(TwibbleUser, username=username)
    followings = profile_user.following.all()
    return render(
        request,
        "users/following_list.html",
        {
            "profile_user": profile_user,
            "followings": followings,
        },
    )


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("users:login")


@login_required
def settings_view(request):
    if request.method == "POST":
        form = TwibbleUserSettingsForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            user = form.save()
            messages.success(request, "Profile updated successfully !")
            username = request.user.username
            # If password was changed, keep the user logged in
            if "password" in form.cleaned_data and form.cleaned_data["password"]:
                update_session_auth_hash(request, user)
            return redirect("users:profile", username=username)
    else:
        form = TwibbleUserSettingsForm(instance=request.user)
    return render(request, "users/settings.html", {"form": form})
