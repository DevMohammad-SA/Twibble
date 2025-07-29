from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TwibbleUser


class TwibbleUserCreationForm(UserCreationForm):
    class Meta:
        model = TwibbleUser
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if TwibbleUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
