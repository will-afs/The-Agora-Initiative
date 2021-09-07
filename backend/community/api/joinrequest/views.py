from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from community.api.joinrequest.serializers import JoinRequestSerializer

from community.models import Community, CommunityMember, JoinRequest

from rest_framework.views import APIView

from community.api.joinrequest.permissions import IsCommunityAdmin, IsCommunityMember
from rest_framework import permissions
from community.utils import community_member_exists, join_request_exists

class JoinRequestList(APIView):
    """
    List all join requests.
    """
    permission_classes = [permissions.IsAuthenticated, IsCommunityAdmin]
    def get(self, request, community_slug:str, format=None):
        community = Community.objects.get(slug=community_slug)
        join_requests = JoinRequest.objects.all().filter(community=community)
        join_requests_serializer = JoinRequestSerializer(join_requests, many=True)
        return Response(join_requests_serializer.data)

class JoinCommunity(APIView):
    """
    Send a join request to the specified community.
    """
    permission_classes = [permissions.IsAuthenticated, ~IsCommunityMember]
    def post(self, request, community_slug):
        data = {}
        author=request.user
        try: 
            community = get_object_or_404(Community, slug=community_slug)
        except Http404:
            data['response'] = 'This community does not exist.'
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data, status_code)

        # author = request.user
        # if community_member_exists(user=author, community=community):
        #     data['response'] = 'This user is already a member of the Community.'
        #     status_code = status.HTTP_400_BAD_REQUEST
        #     return Response(data, status_code)

        if join_request_exists(user=author, community=community):
            data['response'] = 'A join request already exists for this user over the community.'
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data, status_code)

        join_request = JoinRequest(user=author, community=community)
        join_request.save()
        data['response'] = 'Successfully created a join request for user over the community.'
        data['user'] = author.username
        data['community'] = community.name
        status_code = status.HTTP_201_CREATED
        return Response(data, status_code)

class JoinRequestAccept(APIView):
    """
    Accepts the specified join request : creates a new communitymember and removes the join request
    """
    permission_classes = [permissions.IsAuthenticated, IsCommunityAdmin]
    def delete(self, request, join_request_pk:int, community_slug:str, format=None):
        data = {}
        try:
            join_request = get_object_or_404(JoinRequest, pk=join_request_pk)
        except Http404:
            data['response'] = 'This join request does not exist.'
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data, status_code)
        new_community_member = CommunityMember(user=join_request.user, community=join_request.community)
        new_community_member.save()
        # The associated join request is automatically deleted from the signal received at the community member creation
        status_code = status.HTTP_200_OK
        return Response(data, status_code)


class JoinRequestDecline(APIView):
    """
    Declines the specified join request instance : simply removes the join request
    """
    permission_classes = [permissions.IsAuthenticated, IsCommunityAdmin]
    def delete(self, request, join_request_pk:int, community_slug:str, format=None):
        data = {}
        try:
            join_request = get_object_or_404(JoinRequest, pk=join_request_pk)
        except Http404:
            data['response'] = 'This join request does not exist.'
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data, status_code)
        join_request.delete()
        status_code = status.HTTP_200_OK
        return Response(data, status_code)