from rest_framework import serializers

from community.models import Community, JoinRequest

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

# class JoinRequestCreationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Community
#         fields = ['community name', '']

#     def save(self):
#         join_request = JoinRequest(
#             community_name = self.validated_data['community name'],

#         )
#         community.save()
#         return community
