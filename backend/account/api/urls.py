from django.urls import path
from account.api.views import(
    RegistrationView,
    Logout,
    AccountView,
    ChangePasswordView,
    DeleteAccountView
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    path('', AccountView.as_view(), name='detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]