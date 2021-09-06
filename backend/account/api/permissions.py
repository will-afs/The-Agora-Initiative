from rest_framework import permissions
from community.models import Community
from community.utils import is_community_admin
from django.urls import reverse


class AsksToRegister(permissions.BasePermission):
    """
    Custom permission to only allow non authenticated user to register.
    """

    def has_permission(self, request, view): 
        if request.method in ['POST'] and request.path == reverse('account_api:register'):
            return True
        else:
            return False


class AsksToLogin(permissions.BasePermission):
    """
    Custom permission to only allow non authenticated user to login.
    """

    def has_permission(self, request, view): 
        if request.method in ['POST'] and request.path == reverse('account_api:login'):
            return True
        else:
            return False