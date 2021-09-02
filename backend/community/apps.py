from django.apps import AppConfig
from django.db.models.signals import pre_save


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

    def ready(self):
        import community.signals
