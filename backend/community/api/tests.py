from community.models import Community, CommunityMember, JoinRequest
from account.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.template.defaultfilters import slugify


# Helpers
#------------------------------------------------------------


# CONFIGURATION VARIABLES
username = 'testcase'
password = 'somestrongPassword'
email = 'testcase@gmail.com'
community_name = 'CommunityNameExample'
community_slug = slugify(community_name)


# URLS
registration_url = reverse('account_api:register')
login_url = reverse('account_api:login')
create_community_url = reverse('community_api:create_community')
create_join_request_url = reverse(
                                'community_api:join',
                                kwargs={'community_slug':community_slug}
                                )

# DATA
community_data = {
            'name': community_name,
        }
join_request_data = {
    'community name':community_name
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


class JoinRequestCreationTestCase(APITestCase):
    def authenticate(self):
            account = register()
            token_key = get_auth_token(account)[0].key
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_create_join_request_success(self):
        # Create an account and Log on
        self.authenticate() 
        # Create community
        community = Community(name=community_name)
        community.save()
        # Ask to join the community
        self.client.post(create_join_request_url)    

        self.assertEqual(JoinRequest.objects.count(), 1)
        self.assertEqual(JoinRequest.objects.get().user.username, username)
        self.assertEqual(JoinRequest.objects.get().community.name, community_name)

    def test_create_join_request_success(self):
        # Create an account and Log on
        self.authenticate() 
        # Create community
        community = Community(name=community_name)
        community.save()
        # Ask to join the community
        response = self.client.post(create_join_request_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    
        self.assertEqual(JoinRequest.objects.count(), 1)
        self.assertEqual(JoinRequest.objects.get().user.username, username)
        self.assertEqual(JoinRequest.objects.get().community.name, community_name)

    def test_create_join_request_no_auth_fails(self):
        # Create community
        community = Community(name=community_name)
        community.save()
        # Ask to join the community
        response = self.client.post(create_join_request_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
        self.assertEqual(JoinRequest.objects.count(), 0)

    def test_create_join_request_community_does_not_exist_fails(self):
        # Create an account and Log on
        self.authenticate() 
        # Ask to join the community
        response = self.client.post(create_join_request_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    
        self.assertEqual(JoinRequest.objects.count(), 0)

    def test_create_join_request_already_exists_fails(self):
        # Create an account and Log on
        self.authenticate()
        account = Account.objects.get(username=username)
        # Create community
        community = Community(name=community_name)
        community.save()
        # Create a first join request on this community for this user
        join_request = JoinRequest(community=community, user=account)
        join_request.save()
        # Attempt to create a new one
        response = self.client.post(create_join_request_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    
        self.assertEqual(JoinRequest.objects.count(), 1)

    def test_create_join_request_but_already_member_fails(self):
        # Create an account and Log on
        self.authenticate()
        account = Account.objects.get(username=username)
        # Create community
        community = Community(name=community_name)
        community.save()
        # Create a first join request on this community for this user
        community_member = CommunityMember(community=community, user=account)
        community_member.save()
        # Attempt to create a join request but user is already a member of community
        response = self.client.post(create_join_request_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    
        self.assertEqual(JoinRequest.objects.count(), 0)