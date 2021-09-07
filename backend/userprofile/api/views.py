from userprofile.models import UserProfile
from userprofile.api.serializers import UserProfileSerializer
from rest_framework import viewsets
from rest_framework import permissions
from userprofile.api.permissions import IsOwnerOrReadOnly

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve`, `create`, `update` and `partial update` actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
