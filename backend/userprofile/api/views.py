from userprofile.models import UserProfile
from userprofile.api.serializers import UserProfileSerializer
from rest_framework import viewsets

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve` and `update` actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'post', 'head', 'put']
    lookup_field = 'slug'