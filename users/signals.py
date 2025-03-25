from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from carts.models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """
    Create a cart for a user when they register.
    """
    if created:
        Cart.objects.create(user=instance) 