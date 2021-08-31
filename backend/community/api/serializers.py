from account.api.serializers import AccountSerializer
from account.models import Account
from django.template.defaultfilters import join
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from community.models import Community, CommunityMember, JoinRequest
from agorabackend.serializer_utils import RelatedFieldAlternative


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ['name', 'bio']
        lookup_field = 'slug'
        extra_kwargs = {
            'url':{'lookup_field':'slug'}
        }

class CommunityMemberDoesntExistValidator():
        requires_context = True
        missing_message = ('This field is required.')

        def __init__(self, queryset, fields, message=None):
            self.queryset = queryset
            self.fields = fields
            self.message = message or self.message
        
        def __call__(self, user, community):
            if CommunityMember.objects.filter(user=user, community=community).count() != 0:
                message = 'This user is already a member of that community'
                raise serializers.ValidationError(message)

        def set_context(self, serializer_field):
            
            pass

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
                        # # UniqueValidator(
                        # #     queryset=CommunityMember.objects.all(),
                        # #     lookup=['user', 'community'],
                        # #     message='This user is already a member of that community'
                        # # )
                        # CommunityMemberDoesntExistValidator
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