# tweets/forms.py
from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    # We override the widgets here to keep your bootstrap styling
    text = forms.CharField(
        label="",
        max_length=300,
        widget=forms.Textarea(
            attrs={
                "class": "form-control border-0 fs-5 bg-transparent text-body",
                "oninput": "updateCounter()",
                "rows": "4",
                "max_length": "300",
                "placeholder": "What is happening?!",
                "style": "resize: none; box-shadow: none;",
                "id": "tweetText",  # Keep ID for your JS counter
            }
        ),
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "d-none", "id": "imageUpload", "accept": "image/*"}
        ),
    )

    class Meta:
        model = Tweet
        fields = ["text", "image"]
