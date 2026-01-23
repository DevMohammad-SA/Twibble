import re

from django.db import models

from users.models import TwibbleUser

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
    image = models.ImageField(upload_to="tweet_images/", null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tweets")
    bookmarks = models.ManyToManyField(
        TwibbleUser, related_name="bookmarked_tweets", blank=True
    )

    def __str__(self):
        return self.text

    # extract tags automatically
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tags.clear()

        # find hashtags in the text
        # what 're' does here is that it will match the strin that started with # and followed by alphanumeric chars
        hashtags = re.findall(r"#(\w+)", self.text)
        # create or get the tags and add them
        for tag_name in hashtags:
            tag, created = Tag.objects.get_or_create(
                slug=tag_name.lower(), defaults={"name": tag_name}
            )
            self.tags.add(tag)

    @property
    def is_thread(self):
        return self.parent_tweet is not None
