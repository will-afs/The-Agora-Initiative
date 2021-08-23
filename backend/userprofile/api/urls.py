from django.urls import path, include
from rest_framework.routers import DefaultRouter
from userprofile.api import views

app_name = 'userprofile'


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.UserProfileViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls))),
]