from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from account.api.serializers import AccountSerializer, ChangePasswordSerializer, DeleteAccountSerializer
from account.models import Account
from rest_framework import permissions
from account.api.permissions import AsksToRegister
from rest_framework import generics
from community.models import CommunityMember


class RegistrationView(generics.CreateAPIView):
    """
    Register with a new account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [~permissions.IsAuthenticated&AsksToRegister]

    def perform_create(self, serializer):
        account_serializer = serializer
        account = account_serializer.create()
        data = {}
        data['response'] = 'Successfully registered a new user.'
        data['email'] = account.email
        data['username'] = account.username

        # Generate token for further authentication
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status.HTTP_201_CREATED)


class Logout(APIView):
    """
    Log out by deleting the previously generated Auth Token.
    """
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, format=None):
        data = {}
        try :
            # simply delete the token to force a login
            request.user.auth_token.delete()
            data['response'] = 'Successfully logged out.'
            return Response(data=data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            data['response'] = 'User does not exist.'
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class AccountView(generics.RetrieveAPIView): #generics.RetrieveUpdateAPIView
    """
    Retrieve account information.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        data = {}
        try:
            instance = request.user
        except Account.DoesNotExist:
            data['response'] = 'User does not exist.'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
        """
        Change account password.
        """
        serializer_class = ChangePasswordSerializer
        model = Account
        permission_classes = (permissions.IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            data = {}
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    data["old_password"]="Wrong password."
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                data['response'] = 'Successfully changed password.'
                return Response(data=data, status=status.HTTP_200_OK)
                
        def partial_update(self, request, *args, **kwargs):
            data = {'response':'This method is not supported'}
            return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

                
class DeleteAccountView(generics.CreateAPIView):
        """
        Delete the account.
        """
        serializer_class = DeleteAccountSerializer
        model = Account
        permission_classes = (permissions.IsAuthenticated,)

        def last_admin_of_communities(self):
            user = self.request.user
            community_member_list = CommunityMember.objects.filter(user=user, is_admin=True).all()
            communities_slugs = []
            for community_member in community_member_list:
                communities_slugs.append(community_member.community.slug)
            return communities_slugs

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            data = {}
            if serializer.is_valid():
                # Check password
                if not self.object.check_password(serializer.data.get("password")):
                    data["password"]="Wrong password."
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                communities_list = self.last_admin_of_communities()
                if len(communities_list) != 0:
                    message = 'You are the last admin of this community. Please delete it first, or give admin rights to another community member.'
                    for community_slug in communities_list:
                        exec('data[\'' + community_slug + '\']=message')
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.object.delete()
                    data['response'] = 'Successfully deleted the account.'
                    return Response(data=data, status=status.HTTP_200_OK)