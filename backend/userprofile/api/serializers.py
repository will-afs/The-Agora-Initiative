from rest_framework import serializers

from userprofile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['account', 'bio']
        lookup_field = 'slug'
        extra_kwargs = {
            'url':{'lookup_field':'slug'}
        }

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)