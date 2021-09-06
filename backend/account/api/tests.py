from community.models import Community, CommunityMember
from account.api.serializers import AccountSerializer
from django.test.testcases import TestCase
from account.models import Account
from rest_framework.test import APITestCase
from rest_framework import status
from agorabackend.test_utils import APITestCaseWithAuth, register
from rest_framework.authtoken.models import Token


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

class AccountDetailTestCase(APITestCaseWithAuth):
    def test_account_detail_success(self):
        account = self.authenticate()[0]
        response = self.client.get(conf.ACCOUNT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_detail_no_auth_fails(self):
        account = register()
        response = self.client.get(conf.ACCOUNT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_account_partial_edit_username_success(self):
    #     account = self.authenticate()[0]
    #     data = {'username': account.username +'bis'}
    #     response = self.client.patch(conf.ACCOUNT_URL, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['username'], data['username'])
    #     self.assertEqual(account.username, data['username'])

    # def test_account_partial_edit_no_auth_fails(self):
    #     account = register()
    #     data = {'username': account.username +'bis'}
    #     response = self.client.patch(conf.ACCOUNT_URL, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertNotEqual(account.username, data['username'])


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
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(key=token)

    def test_logout_unauthenticated_user_fails(self):
        data={'token':'gdfgdfgdfbdfgbdfbdbdfb'}
        response = self.client.post(conf.LOGOUT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_but_token_already_expired_fails(self):
        [account, token] = self.authenticate()
        data={'token':token}
        account.auth_token.delete() # Token expired
        response = self.client.post(conf.LOGOUT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class DeleteAccountTestCase(APITestCaseWithAuth):
    def test_delete_account_success(self):
        [account, token] = self.authenticate()
        data={'password':conf.PASSWORD_1}
        response = self.client.post(conf.DELETE_ACCOUNT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(pk=account.pk)

    def test_delete_account_wrong_password_fails(self):
        [account, token] = self.authenticate()
        data={'password':conf.PASSWORD_2}
        response = self.client.post(conf.DELETE_ACCOUNT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.filter(pk=account.pk).count(),1)

    def test_delete_account_no_auth_fails(self):
        data={'password':conf.PASSWORD_1}
        response = self.client.post(conf.DELETE_ACCOUNT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_last_admin_fails(self):
        [account, token] = self.authenticate()
        data={'password':conf.PASSWORD_1}
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        community_member = CommunityMember(user=account, community=community, is_admin=True)
        community_member.save()
        response = self.client.post(conf.DELETE_ACCOUNT_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = 'You are the last admin of this community. Please delete it first, or give admin rights to another community member.'
        self.assertEqual(response.data[community.slug], error_msg)



class ChangePasswordTestCase(APITestCaseWithAuth):
    def test_change_password_success(self):
        [account, token] = self.authenticate()
        data = {'old_password': conf.PASSWORD_1, 'new_password': conf.PASSWORD_2}
        response = self.client.patch(conf.CHANGE_PASSWORD_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Account.objects.get(username=account.username)
        self.assertEqual(account.check_password(conf.PASSWORD_2), True)

    # def test_change_password_not_secure_enough_fails(self):
    #     [account, token] = self.authenticate()
    #     data = {'old_password': conf.PASSWORD_1, 'new_password': 'h'}
    #     response = self.client.patch(conf.CHANGE_PASSWORD_URL, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_password_invalid_old_fails(self):
        [account, token] = self.authenticate()
        data = {'old_password': conf.PASSWORD_3, 'new_password': conf.PASSWORD_2}
        response = self.client.patch(conf.CHANGE_PASSWORD_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(account.check_password(conf.PASSWORD_2), False)

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