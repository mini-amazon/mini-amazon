from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    # Cart URLs
    path('', views.cart_view, name='view'),
    path('add/', views.add_to_cart, name='add'),
    path('item/<int:item_id>/update/', views.update_cart_item, name='update_item'),
    path('item/<int:item_id>/remove/', views.remove_from_cart, name='remove_item'),
    path('api/item/<int:item_id>/update/', views.update_cart_item_api, name='update_item_api'),
    path('update/', views.update_cart, name='update'),
    path('clear/', views.clear_cart, name='clear'),
    
    # Checkout URL
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
]
