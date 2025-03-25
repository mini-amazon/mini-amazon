from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', views.change_password_view, name='change_password'),
    path('balance/', views.balance_view, name='balance'),
    path('purchase-history/', views.purchase_history_view, name='purchase_history'),
    path('profile/<int:pk>/', views.public_profile_view, name='public_profile'),
]
