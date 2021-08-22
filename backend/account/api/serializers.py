from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self):
        account = Account.objects.create_user(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            password = self.validated_data['password']
        )
        return account
