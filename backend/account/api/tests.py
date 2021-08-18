import json

from account.api.serializers import RegistrationSerializer
from account.models import Account
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.api.views import registration_view


username = 'testcase'
password = 'somestrongPassword'

class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            'username': username,
            'password': password,
            'email': 'testcase@gmail.com'
        }
        url = reverse('account_api:register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_account_already_exists(self):
        data = {
            'username': username,
            'password': password,
            'email': 'testcase@gmail.com'
        }
        url = reverse('account_api:register')
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field(self):
        data = {
            'username': username,
            'email': 'testcase@gmail.com'
        }
        url = reverse('account_api:register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    
    def test_login_success(self):
               
        # register account
        data = {
            'username': username,
            'password': password,
            'email': 'testcase@gmail.com'
        }
        url = reverse('account_api:register')
        self.client.post(url, data)

        # login onto registered account
        data = {
            'username': username,
            'password': password
        }
        url = reverse('account_api:login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_unregistered_user(self):

        # login onto unregistered user attempt
        data = {
            'username': 'unregisteredusername',
            'password': password
        }
        url = reverse('account_api:login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_fail_wrong_password(self):
        # register account
        data = {
            'username': username,
            'password': password,
            'email': 'testcase@gmail.com'
        }
        url = reverse('account_api:register')
        self.client.post(url, data)

        # login with wrong password attempt
        data = {
            'username': username,
            'password': 'wrongpassword'
        }
        url = reverse('account_api:login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
