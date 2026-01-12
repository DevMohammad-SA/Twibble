from django.test import TestCase
from users.models import TwibbleUser
# Create your tests here.


class UserModelTest(TestCase):

    def test_create_user(self):
        user = TwibbleUser.objects.create_user(
                username="testuser",
                email="test@test.com",
                password="strongpassword@123"
                )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("strongpassword@123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
