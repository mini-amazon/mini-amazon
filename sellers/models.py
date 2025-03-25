from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Inventory(models.Model):
    """
    Model representing a seller's inventory of a product.
    """
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('seller')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=0,
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('inventory item')
        verbose_name_plural = _('inventory items')
        unique_together = ('seller', 'product')
        ordering = ('product__name',)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} @ ${self.price})"
    
    def get_absolute_url(self):
        return reverse('sellers:inventory')
    
    @property
    def is_in_stock(self):
        """
        Check if this inventory item is in stock.
        """
        return self.quantity > 0
    
    @property
    def total_value(self):
        """
        Calculate the total value of this inventory item.
        """
        return self.quantity * self.price
