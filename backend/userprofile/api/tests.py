from rest_framework.test import APITestCase
from account.models import Account
from userprofile.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.template.defaultfilters import slugify

username = 'testcase'
password = 'somestrongPassword'
email = 'testcase@gmail.com'
bio = 'Dummy bio 990097'
user_profile_slug = slugify(username)

user_profile_detail_url = reverse(
                                'userprofile_api:userprofile-detail',
                                kwargs={'slug':user_profile_slug},
                                # kwargs={'userprofile_slug':user_profile_slug},
                                )
user_profiles_url = reverse(
                                'userprofile_api:userprofile-list',
                                )

def register()->Account:
    account = Account.objects.create_user(
            email = email,
            username = username,
            password = password
        )
    return account

def get_auth_token(account:Account)->Token: # Helper method
    token = Token.objects.get_or_create(user=account)
    return token

class UserProfileTestCase(APITestCase):
#     def authenticate(self): 
#             account = register()
#             token_key = get_auth_token(account)[0].key
#             self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_userprofile_created_at_registration_success(self):
        register()
        # Checking an UserProfile has truly been created into the database for the occasion
        self.assertEqual(UserProfile.objects.count(), 1)        
        # Checking this UserProfile has truly been associated to the registered account
        account = Account.objects.get(username=username)
        self.assertEqual(UserProfile.objects.filter(account=account).count(), 1)


#     def test_create_get_profile_success(self):
#         self.authenticate()
#         response = self.client.get(user_profile_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_user_profile_success(self):
#         response = self.client.post(user_profile_detail_url)
#         self.assertEqual(UserProfile.objects.count(), 1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_edit_bio_success(self):
#         self.authenticate()
#         self.assertEqual(UserProfile.objects.count(), 1)
#         response = self.client.put(user_profiles_url, bio)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         #self.assertEqual(UserProfile.objects.get().bio, bio)
