from account.models import Account

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Helpers
#------------------------------------------------------------


username = 'testcase'
password = 'somestrongPassword'
email = 'testcase@gmail.com'

registration_data = {
            'username': username,
            'password': password,
            'email': email
        }

login_data = {
    'username': username,
    'password': password
    }

registration_url = reverse('account_api:register')
login_url = reverse('account_api:login')


def register():
    account = Account.objects.create_user(
            email = email,
            username = username,
            password = password
        )
    return account


#------------------------------------------------------------


class RegistrationTestCase(APITestCase):

    def test_registration_success(self):
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking the account has truly been created into the database
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, username)


    def test_registration_account_already_exists_fails(self):
        register()
        # Trying to register with already used credentials
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created in addition to the previously existing one
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, username)
        

    def test_registration_missing_field_fails(self):
        missing_field_data = {
            'username': username,
            'email': 'testcase@gmail.com'
        }
        response = self.client.post(registration_url, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)

    def test_registration_wrong_username_pattern_fails(self):
        missing_field_data = {
            'username': username+'!',
            'email': email,
            'password':password
        }
        response = self.client.post(registration_url, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)


class LoginTestCase(APITestCase):

    def test_login_success(self):
        register()
        # login onto registered account
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unregistered_user_fails(self):
        # login onto unregistered account
        invalid_username_data = {
            'username': 'unregisteredusername',
            'password': password
        }
        response = self.client.post(login_url, invalid_username_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password_fails(self):
        register()
        # login with invalid password attempt
        invalid_password_data = {
            'username': username,
            'password': 'wrongpassword'
        }
        response = self.client.post(login_url, invalid_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
