from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=300)
    is_verifed = models.BooleanField()
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    def __str__(self):
        return self.username


class Post(models.Model):
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
