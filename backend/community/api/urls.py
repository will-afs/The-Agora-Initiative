from django.urls import path, include
from rest_framework.routers import DefaultRouter
from community.api import views
from rest_framework_nested import routers

app_name = 'community'

router = DefaultRouter()
router.register(r'', views.CommunityViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls))),
    path('<slug:community_slug>/join-requests', views.JoinRequestList.as_view(), name='join-request-list'),
    path('<slug:community_slug>/join-requests/<int:join_request_pk>/accept', views.JoinRequestAccept.as_view(), name='join-request-accept'),
    path('<slug:community_slug>/join-requests/<int:join_request_pk>/decline', views.JoinRequestDecline.as_view(), name='join-request-decline'),
]