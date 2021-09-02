from account.api.serializers import AccountSerializer
from account.models import Account
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from community.models import Community, CommunityMember
from agorabackend.serializer_utils import RelatedFieldAlternative
from community.api.community.serializers import CommunitySerializer


class CommunityMemberSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=Account.objects.all(), serializer=AccountSerializer)
    community = RelatedFieldAlternative(queryset=Community.objects.all(), serializer=CommunitySerializer)
    
    is_admin = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = CommunityMember
        fields = ('user', 'community', 'is_admin')
        validators = [
                        UniqueTogetherValidator(
                            queryset=CommunityMember.objects.all(),
                            fields=['user', 'community'],
                            message='A CommunityMember for this couple of User and Community already exists.'
                        )
                    ]

    def create(self, validated_data):
        """
        Create and return a new `CommunityMember` instance, given the validated data.
        """
        user = validated_data.pop('user')
        community = validated_data.pop('community')
        is_admin = validated_data.pop('is_admin')
        community_member = CommunityMember(user=user, community=community, is_admin=is_admin)
        community_member.save()
        return community_member
            

    def update(self, instance, validated_data):
        """
        Update and return an existing `CommunityMember` instance, given the validated data.
        """
        # Raise an error whether the user or community are attempted to get modified
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.save()
        return instance