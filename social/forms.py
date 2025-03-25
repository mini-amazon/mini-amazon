from django import forms
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import ProductReview, SellerReview, Message
from carts.models import Order


class ProductReviewForm(forms.ModelForm):
    """
    Form for creating and updating product reviews.
    """
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating-select'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': _('Write your review here...')}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        # Add choices for rating
        self.fields['rating'].choices = [(i, str(i)) for i in range(1, 6)]
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.user and not instance.pk:
            instance.user = self.user
            
        if self.product and not instance.pk:
            instance.product = self.product
            
        if commit:
            instance.save()
            
        return instance


class SellerReviewForm(forms.ModelForm):
    """
    Form for creating and updating seller reviews.
    """
    class Meta:
        model = SellerReview
        fields = ['order', 'rating', 'comment']
        widgets = {
            'order': forms.Select(),
            'rating': forms.RadioSelect(attrs={'class': 'rating-select'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': _('Write your review here...')}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.seller = kwargs.pop('seller', None)
        super().__init__(*args, **kwargs)
        
        # Add choices for rating
        self.fields['rating'].choices = [(i, str(i)) for i in range(1, 6)]
        
        # Limit order choices to orders placed by the user with this seller
        if self.user and self.seller:
            self.fields['order'].queryset = Order.objects.filter(
                user=self.user,
                items__inventory__seller=self.seller,
                is_fulfilled=True
            ).distinct()
            
            # If no orders, disable the form
            if not self.fields['order'].queryset.exists():
                for field in self.fields.values():
                    field.disabled = True
                self.add_error(None, _('You must have completed an order with this seller to leave a review.'))
                
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if order is provided
        order = cleaned_data.get('order')
        if not order:
            self.add_error('order', _('You must select an order to review.'))
        
        # Check if user has already reviewed this seller for this order
        if self.user and self.seller and not self.instance.pk:
            order = cleaned_data.get('order')
            if order and SellerReview.objects.filter(user=self.user, seller=self.seller, order=order).exists():
                self.add_error('order', _('You have already reviewed this seller for this order.'))
                
        return cleaned_data
                
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.user and not instance.pk:
            instance.user = self.user
            
        if self.seller and not instance.pk:
            instance.seller = self.seller
            
        if commit:
            instance.save()
            
        return instance


class MessageForm(forms.ModelForm):
    """
    Form for sending messages.
    """
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': _('Type your message here...'),
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.receiver = kwargs.pop('receiver', None)
        self.order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.sender:
            instance.sender = self.sender
            
        if self.receiver:
            instance.receiver = self.receiver
            
        if self.order:
            instance.order = self.order
            
        if commit:
            instance.save()
            
        return instance
