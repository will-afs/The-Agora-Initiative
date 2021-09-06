from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.api.views import(
    RegistrationView,
    Logout,
    AccountView
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'
# registration_router = DefaultRouter()
# registration_router.register(r'', RegistrationViewSet)

urlpatterns = [
    # path('register/', registration_view, name='register'),
    # path('register/', include((registration_router.urls)), name='register'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', AccountView.as_view(), name='detail'),
]