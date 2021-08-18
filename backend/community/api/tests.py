from community.models import Community, CommunityMember
from account.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Helpers
#------------------------------------------------------------


username = 'testcase'
password = 'somestrongPassword'
email = 'testcase@gmail.com'
community_name = 'CommunityNameExample'

registration_url = reverse('account_api:register')
login_url = reverse('account_api:login')
create_community_url = reverse('community_api:create')

community_data = {
            'name': community_name,
        }

def register()->Account: # Helper method
    account = Account(
        username = username,
        email = email,
    )
    account.set_password(password)
    account.save()  
    return account

def get_auth_token(account:Account)->Token: # Helper method
    token = Token.objects.get_or_create(user=account)
    return token


#------------------------------------------------------------


class CommunityCreationTestCase(APITestCase): 
    def authenticate(self):
        account = register()
        token = get_auth_token(account)
        token_key = get_auth_token(account)[0].key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_community_creation_without_auth_fails(self):
        response = self.client.post(create_community_url, community_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Community.objects.count(), 0)

    def test_community_creation_with_correct_auth_success(self):
        self.authenticate()
        response = self.client.post(create_community_url, community_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.get().name, community_name)

    def test_community_creation_already_exists_fails(self):
        self.authenticate()
        self.client.post(create_community_url, community_data) # Community is created
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.get().name, community_name)
        # Community creation attempt while it already exists
        response = self.client.post(create_community_url, community_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.get().name, community_name)

    def test_author_granted_as_admin_member_at_creation(self):
        self.authenticate()
        self.client.post(create_community_url, community_data) # Community is created
        self.assertEqual(CommunityMember.objects.count(), 1)
        self.assertEqual(CommunityMember.objects.get().is_admin, True)
        self.assertEqual(CommunityMember.objects.get().user.username, username)




        