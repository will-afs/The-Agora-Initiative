# import sys
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from account.api.serializers import RegistrationSerializer
from userprofile.models import UserProfile

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        # Register new account
        registration_serializer = RegistrationSerializer(data=request.data)
        data = {}
        if registration_serializer.is_valid():
            account = registration_serializer.save()

            data['response'] = 'Successfully registered a new user. '
            data['email'] = account.email
            data['username'] = account.username

            try:
                # Create user profile
                user = UserProfile(account.pk)
                user.save()
                data['response'] += 'Successfully created user profile. '
            except:
                data['response'] += 'But then, an internal error occured '\
                                    'at user profile creation. ' # + sys.exc_info()[0] + ' '
                account.delete()
                data['response'] += 'Operation cancelled : deleted the previously created account.'
                return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Generate token for further authentication
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = registration_serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(data, status.HTTP_201_CREATED)


