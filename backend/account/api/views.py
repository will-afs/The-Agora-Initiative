# import sys
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from account.api.serializers import AccountSerializer


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        # Register new account
        account_serializer = AccountSerializer(data=request.data)
        data = {}
        if account_serializer.is_valid():
            account = account_serializer.create()

            data['response'] = 'Successfully registered a new user. '
            data['email'] = account.email
            data['username'] = account.username

            # Generate token for further authentication
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = account_serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(data, status.HTTP_201_CREATED)


