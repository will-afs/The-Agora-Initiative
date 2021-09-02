from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CommunityMember, JoinRequest


@receiver(post_save, sender=CommunityMember)
def delete_join_request(sender, instance, created, **kwargs):
    if created:
        # There cannot be any join request associated with an already existing community member
        try:
            join_request = JoinRequest.objects.get(user=instance.user, community=instance.community)
        except JoinRequest.DoesNotExist:
            pass
        else:
            join_request.delete()
