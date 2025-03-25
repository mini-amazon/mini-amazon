from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Model representing a product category.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'category_id': self.pk})

    @property
    def product_count(self):
        return self.product_set.count()


class Product(models.Model):
    """
    Model representing a product.
    """
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('category')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_products',
        verbose_name=_('created by')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        """
        Calculate and return the average rating for this product.
        """
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0

    @property
    def review_count(self):
        """
        Return the number of reviews for this product.
        """
        return self.reviews.count()

    @property
    def sellers(self):
        """
        Return all sellers who have this product in their inventory.
        """
        return self.inventory_items.select_related('seller').all()

    @property
    def min_price(self):
        """
        Return the minimum price of this product across all sellers.
        """
        inventories = self.inventory_items.filter(quantity__gt=0)
        if inventories:
            return min(inventory.price for inventory in inventories)
        return Decimal('0.00')

    def get_average_rating(self):
        """
        Calculate and return the average rating for this product.
        """
        return self.average_rating

    def get_lowest_price(self):
        """
        Return the lowest price of this product.
        """
        return self.min_price
