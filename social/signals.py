from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import Message


@receiver(post_save, sender=Message)
def handle_new_message(sender, instance, created, **kwargs):
    """
    Signal handler for when a new message is created.
    
    In a real-world application, this could send an email or push notification
    to the recipient. For this project, we'll just implement the placeholder.
    """
    if created:
        # For now, we're just implementing the signal hook
        # In a real app, you could send an email or push notification here
        pass 