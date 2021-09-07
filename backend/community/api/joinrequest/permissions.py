from rest_framework import permissions
from community.models import Community
from community.utils import community_member_exists, is_community_admin

class IsCommunityAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins of a community to edit it.
    """

    def has_permission(self, request, view):
        user = request.user
        community_slug = request.parser_context['kwargs']['community_slug']
        community = Community.objects.get(slug=community_slug)
        
        if request.method in ['GET', 'DELETE']:
            if is_community_admin(user=user, community=community):
                return True
        else:
                return False

class IsCommunityMember(permissions.BasePermission):
    """
    Custom permission to only allow admins of a community to edit it.
    """
    def has_permission(self, request, view):
        user = request.user
        community_slug = request.parser_context['kwargs']['community_slug']
        try:
            community = Community.objects.get(slug=community_slug)
        except Community.DoesNotExist:
            return False
        else:
            if community_member_exists(user=user, community=community):
                return True
            else:
                return False