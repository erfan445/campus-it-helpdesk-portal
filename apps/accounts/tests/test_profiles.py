from django.contrib.auth.models import User
from django.test import TestCase
from apps.accounts.models import UserProfile


class ProfileSignalTests(TestCase):
    def test_profile_is_created_for_new_user(self):
        user = User.objects.create_user(username='newuser', password='StrongPass123')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, UserProfile.Role.REQUESTER)
