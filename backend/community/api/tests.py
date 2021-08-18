import json

from community.api.serializers import CommunityCreationSerializer
from account.models import Account
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.api.views import registration_view

username = 'testcase'
password = 'somestrongPassword'
community_name = 'CommunityNameExample'

class CommunityCreationTestCase(APITestCase):

    def authenticate(self): # Helper method
        self.register()
        token_key = self.login()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def register(self): # Helper method
        data = {
            'username': username,
            'password': password,
            'email': username + '@gmail.com',
        }
        url = reverse('account_api:register')
        self.client.post(url, data)

    def login(self)-> str: # Helper method - returns Auth Token as a string
        data = {
            'username': username,
            'password': password,
        }
        url = reverse('account_api:login')
        response = self.client.post(url, data)
        token_key = response.data['token']
        return token_key


    def test_community_creation_without_auth_fails(self):
        data = {
            'name': community_name,
        }
        url = reverse('community_api:create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_community_creation_with_correct_auth_success(self):
        self.authenticate()
        data = {
            'name': community_name,
        }
        url = reverse('community_api:create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        