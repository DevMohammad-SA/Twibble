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
        return redirect("users:profile", user_id=request.user.id)
    # if user is not logged in
    if request.method == "POST":
        authentication_form = TwibbleAuthenticationForm(request.POST, data=request.POST)
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username} !")
            return redirect("users:profile", user_id=user.id)
        else:
            messages.warning(request, "Invalid username or password.")
    else:
        authentication_form = TwibbleAuthenticationForm()

    return render(
        request, "users/login.html", {"authentication_form": authentication_form}
    )


@login_required()
def profile_view(request, user_id):
    user_obj = get_object_or_404(TwibbleUser, pk=user_id)
    return render(request, "users/profile.html", {"user": user_obj})


@login_required()
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("users:login")
