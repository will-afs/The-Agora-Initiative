# import sys
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from community.models import Community, CommunityMember, JoinRequest
from community.api.serializers import CommunityCreationSerializer


# Helpers - Put these functions into a utils.py file or something like this
#------------------------------------------------------------

def community_member_exists(user:Account, community:Community)->bool:
    try:
        CommunityMember.objects.get(community=community, user=user)
        return True
    except CommunityMember.DoesNotExist:
        return False

def join_request_exists(user:Account, community:Community)->bool:
    try:
        JoinRequest.objects.get(community=community, user=user)
        return True
    except JoinRequest.DoesNotExist:
        return False

def community_exists(community_slug:str)->bool:
    try :
            Community.objects.get_object_or_404(slug=community_slug)
            return True
    except Community.DoesNotExist:
        return False


#------------------------------------------------------------


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def create_community_view(request):
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
                return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data = community_creation_serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(data, status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def create_join_request_view(request, community_slug):
    if request.method == 'POST':
        # community_name = request.data['community name']
        community = community_slug
        author = request.user
        data = {} 
        
        try: 
            community = get_object_or_404(Community, slug=community_slug)
        except Http404:
            data['response'] = 'This community does not exist.'
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data, status_code)

        data['user name'] = author.username
        data['community name'] = community.name

        if community_member_exists(user=author, community=community):
            data['response'] = 'This user is already a member of the Community.'
            status_code = status.HTTP_400_BAD_REQUEST # TODO : HTTP_403_FORBIDDEN?
            return Response(data, status_code)

        if join_request_exists(user=author, community=community):
            data['response'] = 'A join request already exists for this user over the community.'
            status_code = status.HTTP_400_BAD_REQUEST # TODO : HTTP_403_FORBIDDEN?
            return Response(data, status_code)

        join_request = JoinRequest(
            community=community,
            user=author
        )
        join_request.save()
        data['response'] = 'Successfully created a join request.'
        status_code = status.HTTP_201_CREATED
        return Response(data, status_code)