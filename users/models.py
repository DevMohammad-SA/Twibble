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
        default="profile_images/default.jpg",
    )  # Consider adding a default profile image attribute as follows : default='path/to/defualt/image.jpg'

    def __str__(self):
        return self.username

