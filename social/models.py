from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductReview(models.Model):
    """
    Model representing a review for a product.
    """
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('product')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='product_reviews',
        verbose_name=_('user')
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    comment = models.TextField(_('comment'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product review')
        verbose_name_plural = _('product reviews')
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.email} for {self.product.name}"

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.product.pk})


class SellerReview(models.Model):
    """
    Model representing a review for a seller.
    """
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_reviews',
        verbose_name=_('seller')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written',
        verbose_name=_('user')
    )
    order = models.ForeignKey(
        'carts.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name=_('order')
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    comment = models.TextField(_('comment'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('seller review')
        verbose_name_plural = _('seller reviews')
        unique_together = ('seller', 'user', 'order')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.email} for {self.seller.email}"

    def get_absolute_url(self):
        return reverse('users:public_profile', kwargs={'pk': self.seller.pk})


class Message(models.Model):
    """
    Model representing a message between users.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('sender')
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name=_('receiver')
    )
    order = models.ForeignKey(
        'carts.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name=_('related order')
    )
    content = models.TextField(_('content'))
    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"

    def get_absolute_url(self):
        # Always use the correct other user's ID consistently
        return reverse('social:conversation', kwargs={'user_id': self.receiver.id})
