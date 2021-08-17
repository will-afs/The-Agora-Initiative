from django.urls import path
from community.api.views import(
    community_creation_view,
)

app_name = 'community'

urlpatterns = [
    path('create', community_creation_view, name='create'),
]