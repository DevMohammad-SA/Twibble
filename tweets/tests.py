from django.test import TestCase
from django.urls import reverse
from tweets.models import Tweet
from users.models import TwibbleUser

class TestLikeView(TestCase):
    def setUp(self):
        self.user = TwibbleUser.objects.create_user(username="user123", password="pass")
        self.tweet = Tweet.objects.create(user=self.user, text="A test tweet")

    def test_like_tweet(self):
        self.client.login(username="user123", password="pass")
        response = self.client.post(reverse("tweets:like", args=[self.tweet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.tweet.likes.filter(id=self.user.id).exists())
