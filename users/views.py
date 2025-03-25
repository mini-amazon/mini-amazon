from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, BalanceUpdateForm, PasswordForm
from .models import User


def register_view(request):
    """
    View for user registration.
    """
    if request.user.is_authenticated:
        messages.info(request, _('You are already logged in.'))
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Account created successfully. Welcome to Mini-Amazon!'))
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    View for user login.
    """
    if request.user.is_authenticated:
        messages.info(request, _('You are already logged in.'))
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Login successful. Welcome back!'))
            
            # Redirect to next page if specified
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    messages.success(request, _('You have been logged out.'))
    return redirect('home')


@login_required
def profile_view(request):
    """
    View for user profile management.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


@login_required
def balance_view(request):
    """
    View for managing user balance.
    """
    if request.method == 'POST':
        form = BalanceUpdateForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            action = form.cleaned_data['action']
            
            if action == 'add':
                request.user.add_to_balance(amount)
                messages.success(request, _('${} has been added to your balance.').format(amount))
            else:  # withdraw
                success = request.user.withdraw_from_balance(amount)
                if success:
                    messages.success(request, _('${} has been withdrawn from your balance.').format(amount))
                else:
                    messages.error(request, _('Insufficient funds for withdrawal.'))
            
            return redirect('users:balance')
    else:
        form = BalanceUpdateForm()
    
    return render(request, 'users/balance.html', {'form': form})


@login_required
def change_password_view(request):
    """
    View for changing user password.
    """
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, _('Your password has been updated.'))
            return redirect('users:profile')
    else:
        form = PasswordForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def purchase_history_view(request):
    """
    View for displaying user's purchase history.
    """
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'users/purchase_history.html', {'orders': orders})


def public_profile_view(request, pk):
    """
    View for public user profile.
    """
    user = get_object_or_404(User, id=pk)
    
    # Get seller reviews if user has any products for sale
    seller_reviews = None
    if user.inventory_items.exists():
        seller_reviews = user.seller_reviews.all().order_by('-created_at')
    
    context = {
        'profile_user': user,
        'seller_reviews': seller_reviews,
    }
    
    return render(request, 'users/public_profile.html', context)
