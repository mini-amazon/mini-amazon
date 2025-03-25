from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'average_rating', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image', 'category')
        }),
        (_('Ownership'), {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
