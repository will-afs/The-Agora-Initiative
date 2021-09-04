from account.api.serializers import AccountSerializer
from django.test.testcases import TestCase
from account.models import Account
from rest_framework.test import APITestCase
from rest_framework import status
from agorabackend.test_utils import APITestCaseWithAuth, register


from agorabackend import test_settings as conf

class RegistrationTestCase(APITestCaseWithAuth):

    def test_registration_success(self):
        response = self.client.post(conf.REGISTRATION_URL, conf.REGISTRATION_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking the account has truly been created into the database
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, conf.USERNAME_1)


    def test_registration_account_already_exists_fails(self):
        register()
        # Trying to register with already used credentials
        response = self.client.post(conf.REGISTRATION_URL, conf.REGISTRATION_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created in addition to the previously existing one
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, conf.USERNAME_1)
        

    def test_registration_missing_field_fails(self):
        missing_field_data = {
            'username': conf.USERNAME_1,
            'email': conf.EMAIL_1
        }
        response = self.client.post(conf.REGISTRATION_URL, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)

    def test_registration_wrong_username_pattern_fails(self):
        missing_field_data = {
            'username': conf.USERNAME_1+'!',
            'email': conf.EMAIL_1,
            'password':conf.PASSWORD_1
        }
        response = self.client.post(conf.REGISTRATION_URL, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking no account has been created
        self.assertEqual(Account.objects.count(), 0)


class LoginTestCase(APITestCase):

    def test_login_success(self):
        register()
        # login onto registered account
        response = self.client.post(conf.LOGIN_URL, conf.LOGIN_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unregistered_user_fails(self):
        # login onto unregistered account
        invalid_username_data = {
            'username': conf.USERNAME_1,
            'password': conf.PASSWORD_1
        }
        response = self.client.post(conf.LOGIN_URL, invalid_username_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password_fails(self):
        register()
        # login with invalid password attempt
        invalid_password_data = {
            'username': conf.USERNAME_1,
            'password': conf.PASSWORD_2 # (Real password is conf.PASSWORD_1)
        }
        response = self.client.post(conf.LOGIN_URL, invalid_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCaseWithAuth):

    def test_logout_success(self):
        # login onto registered account
        [account, token] = self.authenticate()
        data={'token':token}
        response = self.client.post(conf.LOGOUT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthenticated_user_fails(self):
        data={'token':'gdfgdfgdfbdfgbdfbdbdfb'}
        response = self.client.post(conf.LOGOUT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_logout_but_token_already_expired_fails(self):
        [account, token] = self.authenticate()
        data={'token':token}
        account.auth_token.delete() # Token expired
        response = self.client.post(conf.LOGOUT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AccountSerializerTestCase(TestCase):
    def test_account_creation_success(self):
        data = conf.REGISTRATION_DATA_1
        account_serializer = AccountSerializer(data=data)
        self.assertEqual(account_serializer.is_valid(), True)
        account_serializer.create()
        self.assertEqual(Account.objects.count(), 1)

    def test_username_partial_edit_success(self):
        account = register()
        self.assertEqual(Account.objects.count(), 1)
        data = {'username':conf.USERNAME_2}
        account_serializer = AccountSerializer(account, data=data, partial=True)
        self.assertEqual(account_serializer.is_valid(), True)
        account_serializer.save()
        self.assertEqual(Account.objects.filter(username=conf.USERNAME_2).count(), 1)

    def test_wrong_username__partial_edit_fails(self):
        account = register()
        self.assertEqual(Account.objects.count(), 1)
        wrong_username = 'Newu sername'
        data = {'username':wrong_username}
        account_serializer = AccountSerializer(account, data=data, partial=True)
        self.assertEqual(account_serializer.is_valid(), False)
        with self.assertRaises(AssertionError) :
            account_serializer.save()
        self.assertEqual(Account.objects.filter(username=wrong_username).count(), 0)

    def test_password_edit_success(self):
        account = register()
        self.assertEqual(Account.objects.count(), 1)
        data = {'username':conf.USERNAME_2}
        account_serializer = AccountSerializer(account, data=data, partial=True)
        account_serializer.is_valid()
        account_serializer.save()
        self.assertEqual(Account.objects.filter(username=conf.USERNAME_2).count(), 1)

    def test_get_account_serializer_success(self):
        account = register()
        self.assertEqual(Account.objects.count(), 1)
        account_serializer = AccountSerializer(account)
        self.assertEqual(account_serializer.data['username'], conf.USERNAME_1)
        self.assertEqual(account_serializer.data['email'], conf.EMAIL_1)