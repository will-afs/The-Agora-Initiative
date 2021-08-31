from django.urls import path, include
from rest_framework.routers import DefaultRouter
from community.api import views

app_name = 'community'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.CommunityViewSet)
#router.register(r'joinrequests', views.JoinRequestViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls))),
]

# urlpatterns = [
#     path('create', create_community_view, name='create_community'),
#     path('<slug:community_slug>/join', create_join_request_view, name='join'),
# ]