from django.db import models
from django.conf import settings
from django.db.models.fields import related
from tweets.models import Tweet

# Create your models here.


class Notification(models.Model):
    # notification types we want to deal with
    NOTIFICATION_TYPES = (
        ("like", "Like"),
        ("follow", "Follow"),
        ("reply", "Reply"),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # related tweet
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} {self.notification_type} -> {self.recipient}"
