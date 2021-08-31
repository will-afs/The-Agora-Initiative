from rest_framework import permissions
from community.models import CommunityMember

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins of a community to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in ['head', 'options']:
        #     return True
        # elif request.method in ['get']:
        #     # Get permissions are only allowed to CommunityMembers.
        #     if CommunityMember.objects.filter(user=request.user, community=obj).count() == 1:
        #         return True
        if request.method in ['PUT', 'PATCH']:
            # Write permissions are only allowed to admin CommunityMembers.
            if CommunityMember.objects.filter(user=request.user, community=obj, is_admin=True).count() == 1:
                return True
            else:
                return False
        # elif request.method in ['post']:
        #     # Creating a Community is allowed to anybody
        #     return True
        else:
            return True

class IsCommunityMember(permissions.BasePermission):
    """
    Custom permission allowing readonly permission to community members.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            # Get permissions are only allowed to CommunityMembers.
            if CommunityMember.objects.filter(user=request.user, community=obj).count() == 1:
                return True
            else:
                return False
        else:
            return True