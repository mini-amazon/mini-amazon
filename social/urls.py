from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    # Product review URLs
    path('products/<int:product_id>/review/', views.create_product_review, name='product_review'),
    path('product-reviews/<int:review_id>/delete/', views.delete_product_review, name='delete_product_review'),
    
    # Seller review URLs
    path('sellers/<int:seller_id>/review/', views.create_seller_review, name='seller_review'),
    path('seller-reviews/<int:review_id>/delete/', views.delete_seller_review, name='delete_seller_review'),
    
    # User's reviews
    path('my-reviews/', views.UserReviewListView.as_view(), name='my_reviews'),
    
    # Messaging URLs
    path('conversations/', views.conversation_list, name='conversations'),
    path('conversations/<int:user_id>/', views.conversation_detail, name='conversation'),
]
