from rest_framework import permissions
from community.models import CommunityMember

class IsCommunityAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins of a community to edit community member is_admin field.
    """
    def has_object_permission(self, request, view, obj):
        pass
