# post_save bazaga saqlab bulgandan sung ishga tushadi
# pre_save - bazaga saqlashidan oldin ishga tushadi

from django.db.models.signals import post_save
from .models import Account, UserProfile
from django.dispatch import receiver


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

