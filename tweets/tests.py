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

    def test_unlike_tweet_from_likes_tab(self):
        self.client.login(username="user123", password="pass")
        # First like the tweet
        self.tweet.likes.add(self.user)

        # Now unlike it with the correct referer (OWN profile) and headers
        response = self.client.post(
            reverse("tweets:like", args=[self.tweet.id]),
            HTTP_REFERER="http://testserver/users/@user123/?tab=likes",
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.tweet.likes.filter(id=self.user.id).exists())
        self.assertEqual(response.get("HX-Reswap"), "delete")
        self.assertEqual(response.get("HX-Retarget"), f"#tweet-{self.tweet.id}")

    def test_unlike_tweet_from_others_likes_tab(self):
        # Create another user
        TwibbleUser.objects.create_user(username="other", password="pass")
        self.client.login(username="user123", password="pass")

        # user123 likes a tweet
        self.tweet.likes.add(self.user)

        # Now unlike it from OTHER user's profile likes tab
        response = self.client.post(
            reverse("tweets:like", args=[self.tweet.id]),
            HTTP_REFERER="http://testserver/users/@other/?tab=likes",
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.tweet.likes.filter(id=self.user.id).exists())
        # Should NOT have delete headers
        self.assertNotIn("HX-Reswap", response)
        self.assertIn("bi-heart", response.content.decode())
