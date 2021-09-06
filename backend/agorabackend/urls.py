"""agorabackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # REST FRAMEWORK URLS
    path('api/account/', include('account.api.urls', namespace='account_api')),
    path('api/communities/', include('community.api.urls', namespace='community_api')),
    path('api/profiles/', include('userprofile.api.urls', namespace='userprofile_api')),
    path('docs/', include_docs_urls(title='The-Agora-Initiative API')),
    path(
            'api/schema',
            get_schema_view(
                                title='The-Agora-Initiative API',
                                description='API of The-Agora-Initiative back-end',
                                version="v0.1"
                            ),
            name='openapi-schema'
        ),
]   
