from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class TwibbleUser(AbstractUser):
    first_name = None
    last_name = None
    display_name = models.CharField(max_length=50)
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
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System Default"),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="system")

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)
        # Hnadling the Images with Pillow
        if self.profile_image:
            img = Image.open(self.profile_image.path)

            # Set max size in pixels
            max_size = (512, 512)
            # Convert the image max size
            img.thumbnail(max_size)

            # If the image is not RGB, convert it to RGB (to prevent PNG and other extension problems)
            if img.mode != "RGB":
                img = img.convert("RGB")
            # After that save the image
            img.save(self.profile_image.path, quality=85, optimize=True)

    def __str__(self):
        return self.username
