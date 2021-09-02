from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from community.api.joinrequest.serializers import JoinRequestSerializer

from community.models import Community, CommunityMember, JoinRequest

from rest_framework.views import APIView

from community.api.joinrequest.permissions import IsCommunityAdmin
from rest_framework import permissions


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


class JoinRequestAccept(APIView):
    """
    Accept a join request instance : creates a new communitymember and removes the join request
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
    Decline a join request instance : simply removes the join request
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