import importlib
import os
from unittest import mock

from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from tweets.models import Tweet
from twibble import settings as project_settings

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
        self.user = User.objects.create_user(
            username="testuser", password="password", email="testuser@test.com"
        )
        self.client.login(username="testuser", password="password")

        # Create tweets
        self.tweet = Tweet.objects.create(user=self.user, text="Original Tweet")
        self.reply = Tweet.objects.create(
            user=self.user, text="Reply Tweet", is_reply=True, parent_tweet=self.tweet
        )

        # Like a tweet
        self.other_user = User.objects.create_user(
            username="other", password="password", email="other@test.com"
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


class PasswordResetRouteTests(SimpleTestCase):
    def test_password_reset_complete_route_uses_complete_view(self):
        match = resolve(reverse("password_reset_complete"))
        self.assertIs(match.func.view_class, auth_views.PasswordResetCompleteView)


class SettingsEnvParsingTests(SimpleTestCase):
    def test_allowed_hosts_defaults_when_env_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            reloaded_settings = importlib.reload(project_settings)

        self.assertEqual(reloaded_settings.ALLOWED_HOSTS, ["127.0.0.1", "localhost"])

        importlib.reload(project_settings)

    def test_email_env_values_are_cast(self):
        with mock.patch.dict(
            os.environ,
            {"EMAIL_PORT": "2525", "EMAIL_USE_TLS": "false"},
            clear=True,
        ):
            reloaded_settings = importlib.reload(project_settings)

        self.assertEqual(reloaded_settings.EMAIL_PORT, 2525)
        self.assertIs(reloaded_settings.EMAIL_USE_TLS, False)

        importlib.reload(project_settings)
