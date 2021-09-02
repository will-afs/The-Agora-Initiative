from rest_framework import permissions
from community.models import Community
from community.utils import is_community_admin

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
