from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ProductReview, SellerReview, Message


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')
    raw_id_fields = ('product', 'user')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'user', 'order', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('seller__email', 'user__email', 'comment')
    raw_id_fields = ('seller', 'user', 'order')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'get_truncated_content', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'content')
    raw_id_fields = ('sender', 'receiver', 'order')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def get_truncated_content(self, obj):
        """Truncate the message content for display in the admin list view."""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    get_truncated_content.short_description = _('Content')
