from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ('inventory',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_count', 'total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    date_hierarchy = 'created_at'
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('inventory',)
    readonly_fields = ('unit_price', 'fulfilled_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'is_fulfilled', 'created_at')
    list_filter = ('status', 'is_fulfilled', 'created_at')
    search_fields = ('user__email',)
    date_hierarchy = 'created_at'
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'total_amount', 'status', 'is_fulfilled')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'inventory', 'quantity', 'unit_price', 'is_fulfilled')
    list_filter = ('is_fulfilled', 'created_at')
    search_fields = ('order__user__email', 'inventory__product__name')
    readonly_fields = ('order', 'inventory', 'quantity', 'unit_price', 'created_at')
