# import sys
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from account.models import Account
from community.models import Community, CommunityMember
from community.api.serializers import CommunityCreationSerializer


@api_view(['POST'])
def community_creation_view(request):
    if request.method == 'POST':
        # Create a new Community
        community_creation_serializer = CommunityCreationSerializer(data=request.data)
        data = {}
        if community_creation_serializer.is_valid():
            community = community_creation_serializer.save()

            data['response'] = 'Successfully created a new community. '
            data['community name'] = community.name
            #data['admin'] = account.username

            # try:
            #     # Create user profile
            #     user = UserProfile(account)
            #     user.save()
            #     data['response'] += 'Successfully created user profile. '
            # except:
            #     data['response'] += 'But then, an internal error occured '\
            #                         'at user profile creation. ' # + sys.exc_info()[0] + ' '
            #     account.delete()
            #     data['response'] += 'Operation cancelled : deleted the previously created account.'
            #     return Response(data)
        else:
            data = community_creation_serializer.errors
        return Response(data)


