from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import OrderItem, Order


@receiver(post_save, sender=OrderItem)
def update_order_status_on_item_fulfillment(sender, instance, created, **kwargs):
    """
    When an order item is marked as fulfilled, check if all items are fulfilled
    and update the order status accordingly.
    """
    if not created and instance.is_fulfilled:
        # Update order status if all items are fulfilled
        if not OrderItem.objects.filter(order=instance.order, is_fulfilled=False).exists():
            instance.order.is_fulfilled = True
            instance.order.status = 'fulfilled'
            instance.order.save()
        # If some items are fulfilled but not all, set order status to processing
        elif instance.order.status == 'pending':
            instance.order.status = 'processing'
            instance.order.save() 