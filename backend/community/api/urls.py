from django.urls import path
from community.api.views import(
    create_community_view,
    create_join_request_view
)

app_name = 'community'

urlpatterns = [
    path('create', create_community_view, name='create_community'),
    path('<slug:community_slug>/join', create_join_request_view, name='join'),
]