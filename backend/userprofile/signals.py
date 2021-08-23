from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from account.models import Account


@receiver(post_save, sender=Account)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    userprofile = UserProfile.objects.get(account=instance)
    userprofile.save()