import time

from account.api.serializers import AccountSerializer
from django.db import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.models import Account
from community.models import Community, CommunityMember, JoinRequest
from community.api.serializers import CommunitySerializer, JoinRequestSerializer, CommunityMemberSerializer
from rest_framework.views import APIView

from community.api.permissions import IsAdmin, IsCommunityMember
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins

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


class CommunityViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    This viewset automatically provides `post`, `list`, `retrieve`, `create` and `update` actions.
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember, IsAdmin]


    def perform_create(self, serializer):
        community = serializer.save()
        author = self.request.user
        # Grant author as an admin CommunityMember
        admin = CommunityMember(community=community, user=author, is_admin=True)
        admin.save()


    @action(detail=True, methods=['post'])
    def join(self, request, slug):
        data = {}

        try: 
            community = get_object_or_404(Community, slug=slug)
        except Http404:
            data['response'] = 'This community does not exist.'
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data, status_code)

        author = request.user
        if community_member_exists(user=author, community=community):
            data['response'] = 'This user is already a member of the Community.'
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data, status_code)

        if join_request_exists(user=author, community=community):
            data['response'] = 'A join request already exists for this user over the community.'
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data, status_code)

        join_request = JoinRequest(user=author, community=community)
        join_request.save()
        status_code = status.HTTP_201_CREATED
        return Response(data, status_code)


class JoinRequestList(APIView):
    """
    List all join requests.
    """
    def get(self, request, community_slug:str, format=None):
        community = Community.objects.get(slug=community_slug)
        join_requests = JoinRequest.objects.all().filter(community=community)
        join_requests_serializer = JoinRequestSerializer(join_requests, many=True)
        return Response(join_requests_serializer.data)


class JoinRequestAccept(APIView):
    """
    Accept a join request instance : creates a new communitymember and removes the join request
    """
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
    Decline a join request instance : simply removes the join request
    """
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


# class JoinRequestViewSet(mixins.ListModelMixin,
#                         mixins.RetrieveModelMixin,
#                         mixins.DestroyModelMixin,
#                         viewsets.GenericViewSet
#                         ):
#     """
#     This viewset automatically provides `list`, `retrieve`, and `destroy` actions.
#     """
#     queryset = JoinRequest.objects.all()
#     serializer_class = JoinRequestSerializer
#     lookup_field = 'pk' # ['slug', 'pk']
#     permission_classes = [permissions.IsAuthenticated, IsAdmin]

#     def get_queryset(self):
#         return JoinRequest.objects.filter(community=self.kwargs['community_slug'])

#     @action(detail=True, methods=['delete'])
#     def accept(self, request, slug):
#         data = {}
#         try:
#             join_request = get_object_or_404(JoinRequest, id=id)
#         except Http404:
#             data['response'] = 'This community does not exist.'
#             status_code = status.HTTP_404_NOT_FOUND
#             return Response(data, status_code)
#         new_community_member = CommunityMember(user=join_request.user, community = join_request.community)
#         new_community_member.save()
#         # The associated join request should be automatically deleted from the signal received at the community member creation
#         # TODO : JoinRequest deletion should generate a signal that could be caught here
#         status_code = status.HTTP_201_CREATED
#         return Response(data, status_code)

#     @action(detail=True, methods=['delete'])
#     def decline(self, request, slug):
#         join_request = get_object_or_404(JoinRequest, id=id)


