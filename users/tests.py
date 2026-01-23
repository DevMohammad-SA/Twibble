from django.contrib.auth import get_user_model
from django.test import TestCase

from tweets.models import Tweet

# Create your tests here.
User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            display_name="TestUser",
            email="test@test.com",
            password="strongpassword@123",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.display_name, "TestUser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("strongpassword@123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class UserProfileTabsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create tweets
        self.tweet = Tweet.objects.create(user=self.user, text="Original Tweet")
        self.reply = Tweet.objects.create(
            user=self.user, text="Reply Tweet", is_reply=True, parent_tweet=self.tweet
        )

        # Like a tweet
        self.other_user = User.objects.create_user(
            username="other", password="password"
        )
        self.liked_tweet = Tweet.objects.create(
            user=self.other_user, text="Liked Tweet"
        )
        self.liked_tweet.likes.add(self.user)

    def test_posts_tab(self):
        response = self.client.get(f"/users/@{self.user.username}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "posts")
        self.assertIn(self.tweet, response.context["tweets"])
        self.assertNotIn(self.reply, response.context["tweets"])
        self.assertNotIn(self.liked_tweet, response.context["tweets"])

    def test_replies_tab(self):
        response = self.client.get(f"/users/@{self.user.username}/", {"tab": "replies"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "replies")
        self.assertIn(self.reply, response.context["tweets"])
        self.assertNotIn(self.tweet, response.context["tweets"])

    def test_likes_tab(self):
        response = self.client.get(f"/users/@{self.user.username}/", {"tab": "likes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "likes")
        self.assertIn(self.liked_tweet, response.context["tweets"])
        self.assertNotIn(self.tweet, response.context["tweets"])

    def test_media_tab(self):
        response = self.client.get(f"/users/@{self.user.username}/", {"tab": "media"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "media")
        self.assertEqual(response.context["tweets"].count(), 0)

    def test_replies_tab_uses_thread_template(self):
        response = self.client.get(f"/users/@{self.user.username}/", {"tab": "replies"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/_tweet_thread.html")
        self.assertContains(response, "Original Tweet")  # Parent text
        self.assertContains(response, "Reply Tweet")  # Reply text
