from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from account.api.serializers import AccountSerializer, LoginSerializer
from account.models import Account
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import action
from account.api.permissions import AsksToRegister, AsksToLogin
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.db.models import Prefetch
from rest_framework import generics


# class AccountDetail(APIView):
#     """
#     Retrieve, update or delete the user account instance.
#     """
#     def get(self, request, format=None):
#         data={}
#         user=request.user
#         try:
#             account = get_object_or_404(Account, user.pk)
#         except Http404:
#             data['response'] = 'This account does not exist.'
#             status_code = status.HTTP_404_NOT_FOUND
#             return Response(data, status_code)
#         else:
#             account_serializer = AccountSerializer(account)
#             status_code = status.HTTP_200_OK
#             return Response(data=account_serializer.data)


class RegistrationView(generics.CreateAPIView):
    """
    This view automatically provides `create` action in order to register.
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
    This view automatically provides `post` action in order to log out.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try :
            # simply delete the token to force a login
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountView(generics.RetrieveAPIView): #generics.RetrieveUpdateAPIView
    """
    This view automatically provides `get` action in order to manage an account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     try:
    #         instance = request.user
    #     except Account.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)

    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             # If 'prefetch_related' has been applied to a queryset, we need to
    #             # forcibly invalidate the prefetch cache on the instance.
    #             instance._prefetched_objects_cache = {}

    #         return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = request.user
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    

# class DeleteAccountView(generics.CreateAPIView):
#     """
#     This view automatically provides `destroy` action in order to delete an account.
#     """
#     queryset = Account.objects.all()
#     serializer_class = DeleteAccountSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def perform_create(self, request, format=None):
#         data={}
#         try :
#             request.user.delete()
#             data['response'] = 'Account successfully deleted.'   
#             return Response(data, status=status.HTTP_200_OK)
#         except Account.DoesNotExist:
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)


# class ChangePasswordView():
#     """
#     This view automatically provides `post` action in order to delete an account.
#     """
#     queryset = Account.objects.all()
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]

# @api_view(['POST'])
# def registration_view(request):
#     if request.method == 'POST':
#         # Register new account
#         account_serializer = AccountSerializer(data=request.data)
#         data = {}
#         if account_serializer.is_valid():
#             account = account_serializer.create()

#             data['response'] = 'Successfully registered a new user. '
#             data['email'] = account.email
#             data['username'] = account.username

#             # Generate token for further authentication
#             token = Token.objects.get(user=account).key
#             data['token'] = token

#         else:
#             data = account_serializer.errors
#             return Response(data, status.HTTP_400_BAD_REQUEST)
#         return Response(data, status.HTTP_201_CREATED)





