from userprofile.models import UserProfile

from rest_framework import status

from userprofile.api.serializers import UserProfileSerializer
from agorabackend.test_utils import APITestCaseWithAuth
from agorabackend import test_settings as conf
from agorabackend.test_utils import register


class CreateProfileTestCase(APITestCaseWithAuth):

    def test_create_profile_fails(self):
        self.authenticate()
        response = self.client.post(conf.USER_PROFILE_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetUserProfileTestCase(APITestCaseWithAuth):

    def test_get_user_profile_no_auth_fails(self):
        register()
        response = self.client.get(conf.USER_PROFILE_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_own_user_profile_success(self):
        account = self.authenticate()[0]
        response = self.client.get(conf.USER_PROFILE_DETAIL_URL_1)
        userprofile = UserProfile.objects.get(account = account)
        userprofile_serializer = UserProfileSerializer(userprofile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, userprofile_serializer.data)

    def test_get_other_user_profile_success(self):
        account_1 = self.authenticate()[0] # Authenticated with another account (n°2)
        account_2 = register(
                                username=conf.USERNAME_2,
                                email=conf.EMAIL_2,
                                password=conf.PASSWORD_2,
                            )
        user_profile_2_detail_url = conf.USER_PROFILE_DETAIL_URL_2
        response = self.client.get(user_profile_2_detail_url)
        userprofile_2 = UserProfile.objects.get(account = account_2)
        userprofile_2_serializer = UserProfileSerializer(userprofile_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, userprofile_2_serializer.data)


class GetUserProfileListTestCase(APITestCaseWithAuth):

    def test_get_user_profile_list_no_auth_fails(self):
        register()
        response = self.client.get(conf.USER_PROFILES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profiles_list_success(self):
        # Create two user profiles
        account_1 = self.authenticate()[0]
        account_2 = register(
                                username=conf.USERNAME_2,
                                email=conf.EMAIL_2,
                                password=conf.PASSWORD_2,
                            )
        user_profiles_queryset = UserProfile.objects.all()
        user_profiles_serializer = UserProfileSerializer(user_profiles_queryset, many=True)

        response = self.client.get(conf.USER_PROFILES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_profiles_serializer.data)

class EditUserProfileTestCase(APITestCaseWithAuth):

    def test_edit_user_profile_no_auth_fails(self):
        account=register()
        data = {'bio': conf.USER_PROFILE_BIO_2}
        response = self.client.patch(conf.USER_PROFILE_DETAIL_URL_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        userprofile = UserProfile.objects.get(account=account)
        self.assertNotEqual(userprofile.bio, conf.USER_PROFILE_BIO_2)

    def test_edit_user_profile_success(self):
        account=self.authenticate()[0]
        data = {'bio': conf.USER_PROFILE_BIO_2}
        response = self.client.patch(conf.USER_PROFILE_DETAIL_URL_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        userprofile = UserProfile.objects.get(account=account)
        self.assertEqual(userprofile.bio, conf.USER_PROFILE_BIO_2)

    def test_edit_other_user_profile_fails(self):
        account_1 = self.authenticate()[0] # Authenticated with another account (n°2)
        account_2 = register(
                                username=conf.USERNAME_2,
                                email=conf.EMAIL_2,
                                password=conf.PASSWORD_2,
                            )
        user_profile_2_detail_url = conf.USER_PROFILE_DETAIL_URL_2
        data = {'bio': conf.USER_PROFILE_BIO_1}
        response = self.client.patch(user_profile_2_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        userprofile = UserProfile.objects.get(account=account_1)
        self.assertNotEqual(userprofile.bio, conf.USER_PROFILE_BIO_1)


class DeleteProfileTestCase(APITestCaseWithAuth):

    def test_delete_profile_fails(self):
        self.authenticate()
        response = self.client.delete(conf.USER_PROFILE_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserProfile.objects.count(), 1)



