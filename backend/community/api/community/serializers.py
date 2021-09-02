
from rest_framework import serializers

from community.models import Community

class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ['name', 'bio']
        lookup_field = 'slug'
        extra_kwargs = {
            'url':{'lookup_field':'slug'}
        }