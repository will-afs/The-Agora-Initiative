from rest_framework import serializers

from account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']


        def save(self):
            account = Account(
                email = self.validated_data['email'],
                username = self.validated_data['username'],
            )
            password = self.validated_data['password']
            account.set_password(password)
            account.save()
            return account
