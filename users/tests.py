from django.contrib.auth import get_user_model
from django.test import TestCase

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
