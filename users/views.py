from django.shortcuts import render, redirect
from .forms import TwibbleUserCreationForm
from .models import TwibbleUser


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
    return render(request, "users/login.html")
