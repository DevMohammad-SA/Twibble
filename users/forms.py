from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext as _

from .models import TwibbleUser


class TwibbleUserCreationForm(UserCreationForm):
    display_name = forms.CharField(
        max_length=50,
        required=True,
        label=_("Display Name"),
        help_text="Your public name.",
    )

    class Meta:
        model = TwibbleUser
        fields = ["username", "display_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if TwibbleUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email address is already in use"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        if TwibbleUser.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username is already in use"))
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TwibbleAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username or Email"))

    def clean_username(self):
        username_input = self.cleaned_data.get("username").lower()
        user_model = get_user_model()
        try:
            # check if the input is Email
            if "@" in username_input:
                user = get_user_model().objects.get(email=username_input)
            else:  # if the input is the user name
                user = get_user_model().objects.get(username=username_input)
            self.cleaned_data["username"] = user.username
        except user_model.DoesNotExist:
            raise forms.ValidationError("User does not exist.") from None
        return self.cleaned_data["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TwibbleUserSettingsForm(forms.ModelForm):
    display_name = forms.CharField(
        max_length=50,
        required=True,
        label=_("Display Name"),
        help_text=_("Your public name."),
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label=_("Profile Image"),
    )
    password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave blank if you don't want to change your password"),
    )
    bio = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=_("Bio"),
        validators=[
            MaxLengthValidator(
                300,
                message=_("Your bio cannot exceed 300 charactars!"),
            )
        ],
    )

    class Meta:
        model = TwibbleUser
        fields = [
            "profile_image",
            "username",
            "display_name",
            "email",
            "bio",
            "theme",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
