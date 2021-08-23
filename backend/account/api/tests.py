from account.models import Account
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from agorabackend.test_utils import APITestCaseWithAuth, register


from agorabackend import test_settings as conf

class RegistrationTestCase(APITestCaseWithAuth):

    def test_registration_success(self):
        response = self.client.post(conf.REGISTRATION_URL, conf.REGISTRATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking the account has truly been created into the database
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, conf.USERNAME)


    def test_registration_account_already_exists_fails(self):
        register()
        # Trying to register with already used credentials
        response = self.client.post(conf.REGISTRATION_URL, conf.REGISTRATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created in addition to the previously existing one
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, conf.USERNAME)
        

    def test_registration_missing_field_fails(self):
        missing_field_data = {
            'username': conf.USERNAME,
            'email': 'testcase@gmail.com'
        }
        response = self.client.post(conf.REGISTRATION_URL, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)

    def test_registration_wrong_username_pattern_fails(self):
        missing_field_data = {
            'username': conf.USERNAME+'!',
            'email': conf.EMAIL,
            'password':conf.PASSWORD
        }
        response = self.client.post(conf.REGISTRATION_URL, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)


class LoginTestCase(APITestCase):

    def test_login_success(self):
        register()
        # login onto registered account
        response = self.client.post(conf.LOGIN_URL, conf.LOGIN_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unregistered_user_fails(self):
        # login onto unregistered account
        invalid_username_data = {
            'username': 'unregisteredusername',
            'password': conf.PASSWORD
        }
        response = self.client.post(conf.LOGIN_URL, invalid_username_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password_fails(self):
        register()
        # login with invalid password attempt
        invalid_password_data = {
            'username': conf.USERNAME,
            'password': 'wrongpassword'
        }
        response = self.client.post(conf.LOGIN_URL, invalid_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
