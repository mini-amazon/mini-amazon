from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cart(models.Model):
    """
    Model representing a user's shopping cart.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f"{self.user.email}'s Cart"
    
    def get_absolute_url(self):
        return reverse('carts:view')
    
    @property
    def total(self):
        """
        Calculate the total cost of all items in the cart.
        """
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def item_count(self):
        """
        Get the number of items in the cart.
        """
        return self.items.count()
    
    def clear(self):
        """
        Remove all items from the cart.
        """
        self.items.all().delete()


class CartItem(models.Model):
    """
    Model representing an item in a shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('cart')
    )
    inventory = models.ForeignKey(
        'sellers.Inventory',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name=_('inventory')
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        unique_together = ('cart', 'inventory')

    def __str__(self):
        return f"{self.quantity} x {self.inventory.product.name}"
    
    @property
    def subtotal(self):
        """
        Calculate the subtotal for this cart item.
        """
        return self.quantity * self.inventory.price


class Order(models.Model):
    """
    Model representing a customer order.
    """
    ORDER_STATUS = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('fulfilled', _('Fulfilled')),
        ('cancelled', _('Cancelled')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('user')
    )
    total_amount = models.DecimalField(
        _('total amount'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=ORDER_STATUS,
        default='pending'
    )
    is_fulfilled = models.BooleanField(_('is fulfilled'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    
    def get_absolute_url(self):
        return reverse('carts:order_detail', kwargs={'pk': self.pk})
    
    def update_status(self):
        """
        Update the status of the order based on fulfillment of items.
        """
        if self.status == 'cancelled':
            return
            
        if self.items.filter(is_fulfilled=False).exists():
            # At least one item not fulfilled
            if self.status == 'pending':
                self.status = 'processing'
        else:
            # All items fulfilled
            self.status = 'fulfilled'
            self.is_fulfilled = True
            
        self.save()


class OrderItem(models.Model):
    """
    Model representing an item within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order')
    )
    inventory = models.ForeignKey(
        'sellers.Inventory',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('inventory')
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        _('unit price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_fulfilled = models.BooleanField(_('is fulfilled'), default=False)
    fulfilled_at = models.DateTimeField(_('fulfilled at'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f"{self.quantity} x {self.inventory.product.name}"
    
    @property
    def subtotal(self):
        """
        Calculate the subtotal for this order item.
        """
        return self.quantity * self.unit_price
    
    def mark_fulfilled(self):
        """
        Mark this item as fulfilled and update the parent order status.
        """
        from django.utils import timezone
        
        self.is_fulfilled = True
        self.fulfilled_at = timezone.now()
        self.save()
        
        # Update the order status
        self.order.update_status()
