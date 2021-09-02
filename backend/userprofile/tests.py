from django.test import TestCase
from agorabackend.test_utils import register
from userprofile.models import UserProfile


class UserProfileTestCase(TestCase):
    def test_userprofile_created_at_registration_success(self):
            account = register()
            # Checking an UserProfile has truly been created into the database for the occasion
            self.assertEqual(UserProfile.objects.count(), 1)        
            # Checking this UserProfile has truly been associated to the registered account
            self.assertEqual(UserProfile.objects.filter(account=account).count(), 1)