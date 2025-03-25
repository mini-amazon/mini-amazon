from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User
from decimal import Decimal


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    full_name = forms.CharField(
        label=_('Full Name'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'})
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'address', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    """
    Form for user login.
    """
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile.
    """
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )
    full_name = forms.CharField(
        label=_('Full Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'address']


class BalanceUpdateForm(forms.Form):
    """
    Form for adding or withdrawing from balance.
    """
    amount = forms.DecimalField(
        label=_('Amount'),
        min_value=Decimal('0.01'),
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'})
    )
    
    TRANSACTION_CHOICES = [
        ('add', _('Add to Balance')),
        ('withdraw', _('Withdraw from Balance')),
    ]
    
    action = forms.ChoiceField(
        label=_('Transaction Type'),
        choices=TRANSACTION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )


class PasswordForm(PasswordChangeForm):
    """
    Form for changing password.
    """
    old_password = forms.CharField(
        label=_('Current Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
