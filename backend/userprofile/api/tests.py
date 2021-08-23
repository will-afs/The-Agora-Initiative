from rest_framework.test import APITestCase
from account.models import Account
from userprofile.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

from userprofile.api.serializers import UserProfileSerializer
from agorabackend.test_utils import APITestCaseWithAuth
from agorabackend import test_settings as conf
from agorabackend.test_utils import register


class UserProfileTestCase(APITestCaseWithAuth):

    def test_edit_user_profile_success(self):
        account=register()
        data = {'bio': 'New bio'}
        response = self.client.put(conf.USER_PROFILE_DETAIL_URL, data=data)
        userprofile = UserProfile.objects.get(account=account)
        self.assertEqual(userprofile.bio, 'New bio')

    def test_get_user_profile_success(self):
        account = self.authenticate()[0]
        userprofile = UserProfile.objects.get(account = account)
        userprofile_serializer = UserProfileSerializer(userprofile)
        response = self.client.get(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, userprofile_serializer.data)
    
    def test_get_profiles_list_success(self):
        # Create two user profiles
        register()
        register(
                    username='otheruser',
                    password='testpassword',
                    email='otheruser@gmail.com'
                )
        user_profiles_queryset = UserProfile.objects.all()
        user_profiles_serializer = UserProfileSerializer(user_profiles_queryset, many=True)

        response = self.client.get(conf.USER_PROFILES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_profiles_serializer.data)

    def test_delete_profile_fails(self):
        register()
        response = self.client.delete(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_create_profile_fails(self):
        response = self.client.post(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserProfile.objects.count(), 0)

