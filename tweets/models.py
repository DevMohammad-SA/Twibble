from django.db import models
from users.models import TwibbleUser
# Create your models here.
class Tweet(models.Model):
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_reply = models.BooleanField(default=False)
    user = models.ForeignKey(TwibbleUser, on_delete=models.CASCADE)
