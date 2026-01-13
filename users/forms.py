from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MaxLengthValidator
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
        username = self.cleaned_data.get("username")
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


class TwibbleUserSettingsForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change your password",
    )
    bio = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Bio",
        validators=[
            MaxLengthValidator(
                300,
                message="Your bio cannot exceed 300 charactars!",
            )
        ],
    )

    class Meta:
        model = TwibbleUser
        fields = [
            "profile_image",
            "username",
            "first_name",
            "last_name",
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
