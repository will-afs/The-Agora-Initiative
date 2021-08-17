# import sys
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from account.models import Account
from community.models import Community, CommunityMember
from community.api.serializers import CommunityCreationSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def community_creation_view(request):
    if request.method == 'POST':
        # Create a new Community
        community_creation_serializer = CommunityCreationSerializer(data=request.data)
        data = {}
        if community_creation_serializer.is_valid():
            community = community_creation_serializer.save()

            data['response'] = 'Successfully created a new community. '
            data['community name'] = community.name

            try:
                # Grant author as an admin CommunityMember
                author = request.user
                admin = CommunityMember(community=community, user=author, is_admin=True)
                admin.save()
                data['response'] += 'Successfully granted author as admin. '
                data['admin username'] = author.username
            except:
                data['response'] += 'But then, an internal error occured '\
                                    'when trying to grant author as community admin. ' # + sys.exc_info()[0] + ' '
                community.delete()
                data['response'] += 'Operation cancelled : deleted the previously created community.'
                return Response(data)
        else:
            data = community_creation_serializer.errors
        return Response(data)


