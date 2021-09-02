from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from account.models import Account
from userprofile.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status

from userprofile.api.serializers import UserProfileSerializer
from agorabackend.test_utils import APITestCaseWithAuth
from agorabackend import test_settings as conf
from agorabackend.test_utils import register
from django.template.defaultfilters import slugify
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

from account.api.serializers import AccountSerializer


class CreateProfileTestCase(APITestCaseWithAuth):

    def test_create_profile_fails(self):
        self.authenticate()
        response = self.client.post(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetUserProfileTestCase(APITestCaseWithAuth):

    def test_get_user_profile_no_auth_fails(self):
        register()
        response = self.client.get(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_own_user_profile_success(self):
        account = self.authenticate()[0]
        response = self.client.get(conf.USER_PROFILE_DETAIL_URL)
        userprofile = UserProfile.objects.get(account = account)
        userprofile_serializer = UserProfileSerializer(userprofile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, userprofile_serializer.data)

    def test_get_other_user_profile_success(self):
        account_1 = register(
                                username='OtherTestAccount',
                                email='othertestaccount@gmail.com',
                                password='dummypwd'
                            )
        self.authenticate()[0] # Authenticated with another account (n°2)
        user_profile_1_detail_url = reverse(
                                'userprofile_api:userprofile-detail',
                                kwargs={'slug':slugify(account_1.username)},
                                )
        response = self.client.get(user_profile_1_detail_url)
        userprofile_1 = UserProfile.objects.get(account = account_1)
        userprofile_1_serializer = UserProfileSerializer(userprofile_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, userprofile_1_serializer.data)


class GetUserProfileListTestCase(APITestCaseWithAuth):

    def test_get_user_profile_list_no_auth_fails(self):
        register()
        response = self.client.get(conf.USER_PROFILES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profiles_list_success(self):
        # Create two user profiles
        self.authenticate()
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

class EditUserProfileTestCase(APITestCaseWithAuth):

    def test_edit_user_profile_no_auth_fails(self):
        account=register()
        data = {'bio': 'New bio'}
        response = self.client.patch(conf.USER_PROFILE_DETAIL_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        userprofile = UserProfile.objects.get(account=account)
        self.assertNotEqual(userprofile.bio, 'New bio')

    def test_edit_user_profile_success(self):
        account=self.authenticate()[0]
        data = {'bio': 'New bio'}
        response = self.client.patch(conf.USER_PROFILE_DETAIL_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        userprofile = UserProfile.objects.get(account=account)
        self.assertEqual(userprofile.bio, 'New bio')

    def test_edit_other_user_profile_fails(self):
        account_1 = register(
                                username='OtherTestAccount',
                                email='othertestaccount@gmail.com',
                                password='dummypwd'
                            )
        self.authenticate()[0] # Authenticated with another account (n°2)
        user_profile_1_detail_url = reverse(
                                'userprofile_api:userprofile-detail',
                                kwargs={'slug':slugify(account_1.username)},
                                )
        data = {'bio': 'New bio'}
        response = self.client.patch(user_profile_1_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        userprofile = UserProfile.objects.get(account=account_1)
        self.assertNotEqual(userprofile.bio, 'New bio')


class DeleteProfileTestCase(APITestCaseWithAuth):

    def test_delete_profile_fails(self):
        self.authenticate()
        response = self.client.delete(conf.USER_PROFILE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserProfile.objects.count(), 1)



