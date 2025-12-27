from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class TwibbleUser(AbstractUser):
    bio = models.TextField(max_length=300, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True,
        default="static/images/default-avatar.jpg",
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
