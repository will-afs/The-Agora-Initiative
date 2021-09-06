from account.models import Account
from agorabackend import test_settings as conf
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


def register(username=conf.USERNAME_1, password=conf.PASSWORD_1, email=conf.EMAIL_1)->Account:
    account = Account.objects.create_user(
            username = username,
            email = email,
            password = password,
        )
    return account

def get_auth_token(account:Account)->Token: # Helper method
    token = Token.objects.get_or_create(user=account)
    return token



class APITestCaseWithAuth(APITestCase):
    def authenticate(self, username=conf.USERNAME_1, password=conf.PASSWORD_1, email=conf.EMAIL_1): 
        account = register(username=username, password=password, email=email)
        token_key = get_auth_token(account=account)[0].key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)
        return account, token_key
        
    def logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='')