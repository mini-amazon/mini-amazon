from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Category URLs
    path('categories/', views.category_list, name='categories'),
    path('category/<int:category_id>/', views.ProductListView.as_view(), name='category'),
    
    # Product URLs
    path('', views.ProductListView.as_view(), name='list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='update'),
    
    # Search URL
    path('search/', views.ProductSearchView.as_view(), name='search'),
]
