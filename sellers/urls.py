from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    # Inventory URLs
    path('inventory/', views.InventoryListView.as_view(), name='inventory'),
    path('inventory/create/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/update/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),
    path('inventory/quick-add/', views.quick_add_to_inventory, name='quick_add_inventory'),
    
    # Order fulfillment URLs
    path('fulfillment/', views.OrderFulfillmentListView.as_view(), name='order_fulfillment'),
    path('fulfillment/item/<int:item_id>/fulfill/', views.fulfill_order_item, name='fulfill_order_item'),
    
    # Analytics URL
    path('analytics/', views.SalesAnalyticsView.as_view(), name='sales_analytics'),
]
