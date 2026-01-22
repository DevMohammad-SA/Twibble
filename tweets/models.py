from django.db import models

from users.models import TwibbleUser

# Create your models here.


class Tweet(models.Model):
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)
    parent_tweet = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    is_pinned = models.BooleanField(default=False)
    user = models.ForeignKey(
        TwibbleUser, on_delete=models.CASCADE, related_name="tweets"
    )
    likes = models.ManyToManyField(TwibbleUser, related_name="liked_tweets", blank=True)

    def __str__(self):
        return self.text

    @property
    def is_thread(self):
        return self.parent is not None
