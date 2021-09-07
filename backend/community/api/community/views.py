from django.http.response import Http404
from django.shortcuts import get_object_or_404
from community.models import Community, CommunityMember, JoinRequest
from community.api.community.serializers import CommunitySerializer
from rest_framework import status
from rest_framework.response import Response


from community.api.community.permissions import IsCommunityAdmin, IsCommunityMember
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import action
from community.utils import community_member_exists, join_request_exists


class CommunityViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    This viewset automatically provides `create`, `retrieve`, `list`, `update` and `join` actions.
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember, IsCommunityAdmin]


    def perform_create(self, serializer):
        community = serializer.save()
        author = self.request.user
        # Grant author as an admin CommunityMember
        admin = CommunityMember(community=community, user=author, is_admin=True)
        admin.save()
