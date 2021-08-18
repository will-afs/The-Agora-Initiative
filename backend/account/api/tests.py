import json

from account.api.serializers import RegistrationSerializer
from account.models import Account
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.api.views import registration_view

class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            'username': 'registrationtestcase',
            'email': 'registrationtestcase@gmail.com',
            'password': 'somestrongPassword'
        }
        url = reverse('account_api:register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
