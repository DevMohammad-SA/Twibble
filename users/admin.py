from django.contrib import admin
from .models import TwibbleUser, Post

# Register your models here.
admin.site.register(TwibbleUser)
admin.site.register(Post)
