from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TwibbleUserCreationForm, TwibbleAuthenticationForm
from .models import TwibbleUser
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here
def register_view(request):
    if request.method == "POST":
        form = TwibbleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have signed up successfully.")
            return redirect("users:login")
    else:
        form = TwibbleUserCreationForm()
    return render(request, "users/register.html", {"form": form})


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
    tweets = profile_user.tweets.all().order_by("-created_at")
    current_user = request.user
    #Check if current_user is already following profile_user
    already_following = profile_user in current_user.following.all()

    context = {
        "profile_user": profile_user,
        "tweets": tweets,
        "current_user": current_user,
        "already_following":already_following,
    }
    return render(request, "users/profile.html", context)

@login_required
def follow_view(request,username):
    profile_user = get_object_or_404(TwibbleUser,username=username)
    if request.user != profile_user:
        request.user.following.add(profile_user)
    else:
        messages.error(request,"You cannot follow yourself")
    return redirect("users:profile",username=username)


@login_required
def unfollow_view(request,username):
    profile_user = get_object_or_404(TwibbleUser,username=username)
    if request.user != profile_user:
        request.user.following.remove(profile_user)
    return redirect("users:profile",username=username)

@login_required
def followers_list_view(request,username):
    profile_user = get_object_or_404(TwibbleUser,username=username)
    followers = profile_user.followers.all()
    return render(request,"users/followers_list.html",{
        "profile_user":profile_user,
        "followers":followers,
    })

@login_required
def following_list_view(request,username):
    profile_user = get_object_or_404(TwibbleUser,username=username)
    followings = profile_user.following.all()
    return render(request,"users/following_list.html",{
        "profile_user" : profile_user,
        "followings" :  followings,
    } )

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("users:login")
