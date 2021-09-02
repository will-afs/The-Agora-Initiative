from account.api.serializers import AccountSerializer
from account.models import Account
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from community.models import Community, CommunityMember, JoinRequest
from agorabackend.serializer_utils import RelatedFieldAlternative
from community.api.community.serializers import CommunitySerializer


class JoinRequestSerializer(serializers.ModelSerializer):
    user = RelatedFieldAlternative(queryset=Account.objects.all(), serializer=AccountSerializer)
    community = RelatedFieldAlternative(queryset=Community.objects.all(), serializer=CommunitySerializer)
    creation_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = JoinRequest
        fields = ('user', 'community', 'creation_date')
        validators = [
                        UniqueTogetherValidator(
                            queryset=JoinRequest.objects.all(),
                            fields=['user', 'community'],
                            message='A Join Request for this couple of User and Community already exists.'
                        ),
                    ]
    
    def validate(self, data):
        """
        Check that the user is not already a member of the community
        """
        try :
            if CommunityMember.objects.filter(user=data['user'], community=data['community']).count() != 0:
                message = 'This user is already a member of that community'
                raise serializers.ValidationError(message)
            return data
        except KeyError:
            # Means partial update method is called, which should not do anything
            return data

    def create(self, validated_data):
        user = validated_data.pop('user')
        community = validated_data.pop('community')
        join_request = JoinRequest(
                                        user=user, 
                                        community=community, 
                                    )
        join_request.save()
        return join_request

    def update(self, instance, validated_data):
        """
        By default, update() would update the fields given the validated data.
        None of the JoinRequest fields should be modified after its creation.
        Thus, this method has to be overloaded.
        Returns the provided `CommunityMember` instance, without any modification.
        """
        return instance