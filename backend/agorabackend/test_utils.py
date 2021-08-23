from typing import List
from account.models import Account
from agorabackend import test_settings as conf 
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


def register(username=conf.USERNAME, password=conf.PASSWORD, email=conf.EMAIL)->Account:
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
    def authenticate(self): 
            account = register()
            token_key = get_auth_token(account)[0].key
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)
            return account,token_key