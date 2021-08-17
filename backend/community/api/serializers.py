from rest_framework import serializers

from community.models import Community

class CommunityCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ['name']

    def save(self):
        community = Community(
            name = self.validated_data['name'],
        )
        community.save()
        return community
