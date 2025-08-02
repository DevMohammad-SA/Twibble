from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TwibbleUserCreationForm, TwibbleAuthenticationForm
from .models import TwibbleUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse


# Create your views here
def register_view(request):
    if request.method == "POST":
        form = TwibbleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = TwibbleUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        user = authentication_form.get_user()
        return redirect("users:profile", user_id=user.id)

    if request.method == "POST":
        authentication_form = TwibbleAuthenticationForm(
            request.POST, data=request.POST)
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user)
            return redirect("users:profile", user_id=user.id)
    else:
        authentication_form = TwibbleAuthenticationForm()

    return render(
        request, "users/login.html", {
            "authentication_form": authentication_form}
    )


@login_required()
def profile_view(request, user_id):
    user_obj = get_object_or_404(TwibbleUser, pk=user_id)
    return render(request, "users/profile.html", {"user": user_obj})


@login_required()
def logout_view(request):
    logout(request)
    return redirect("users:login")
