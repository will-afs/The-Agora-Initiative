from rest_framework import serializers

from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

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

# class SetPasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['username', 'password']
#         extra_kwargs = {'password':{'write_only':True}}

#     def update(self, request, *args, **kwargs):
#         account = self.get_object()
#         password = self.validated_data['password']
#         account.set_password()
        

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self):
        account = Account.objects.create_user(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            password = self.validated_data['password'],
        )
        return account


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def get(self):
        account = Account.objects.create_user(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            password = self.validated_data['password'],
        )
        return account
        
    # def update(self, request, *args, **kwargs):
    #     account = Account.objects.get(username=self.data['username'])
    #     account_serializer = AccountSerializer(account)

    #     account_serializer
    #     account.username = 
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return serializer.data # Response(serializer.data)
