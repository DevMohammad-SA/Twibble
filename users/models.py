from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class TwibbleUser(AbstractUser):
    bio = models.TextField(max_length=300, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True,
        default="profile_images/default-avatar.jpg",
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)

            max_size = (512,512)
            img.thumbnail(max_size)

            if img.mode != "RGB":
                img = img.convert("RGB")
            
            img.save(self.profile_image.path, quality=85, optimize=True)

    def __str__(self):
        return self.username
