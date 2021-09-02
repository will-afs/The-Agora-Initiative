from django.urls import path, include
from rest_framework.routers import DefaultRouter
from community.api.joinrequest.views import JoinRequestList, JoinRequestAccept, JoinRequestDecline
from community.api.community.views import CommunityViewSet


app_name = 'community'

router = DefaultRouter()
router.register(r'', CommunityViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls))),
    path('<slug:community_slug>/join-requests', JoinRequestList.as_view(), name='join-request-list'),
    path('<slug:community_slug>/join-requests/<int:join_request_pk>/accept', JoinRequestAccept.as_view(), name='join-request-accept'),
    path('<slug:community_slug>/join-requests/<int:join_request_pk>/decline', JoinRequestDecline.as_view(), name='join-request-decline'),
]