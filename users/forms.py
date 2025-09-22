from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import TwibbleUser


class TwibbleUserCreationForm(UserCreationForm):
    class Meta:
        model = TwibbleUser
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if TwibbleUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use")
        return email.lower()
    def clean_username(self):
        username= self.cleaned_data.get("username")
        if TwibbleUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use")
        return username.lower()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TwibbleAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean_username(self):
        username_input = self.cleaned_data.get("username").lower()
        UserModel = get_user_model()
        try:
            # check if the input is Email
            if "@" in username_input:
                user = get_user_model().objects.get(email=username_input)
            else:  # if the input is the user name
                user = get_user_model().objects.get(username=username_input)
            self.cleaned_data["username"] = user.username
        except UserModel.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        return self.cleaned_data["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
