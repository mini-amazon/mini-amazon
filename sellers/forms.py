from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

from .models import Inventory
from products.models import Product


class InventoryForm(forms.ModelForm):
    """
    Form for creating and updating inventory items.
    """
    class Meta:
        model = Inventory
        fields = ['product', 'quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'price': forms.NumberInput(attrs={'min': 0.01, 'step': 0.01}),
        }

    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('seller', None)
        super().__init__(*args, **kwargs)
        
        # If this is an update, don't allow changing the product
        if self.instance.pk:
            self.fields['product'].disabled = True
            
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < Decimal('0.01'):
            raise forms.ValidationError(_('Price must be at least $0.01.'))
        return price
        
    def clean(self):
        cleaned_data = super().clean()
        
        # If this is a new inventory item, check if the seller already has this product
        if not self.instance.pk and self.seller:
            product = cleaned_data.get('product')
            if product and Inventory.objects.filter(seller=self.seller, product=product).exists():
                self.add_error('product', _('You already have this product in your inventory.'))
                
        return cleaned_data
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.seller and not instance.pk:
            instance.seller = self.seller
            
        if commit:
            instance.save()
            
        return instance


class QuickAddInventoryForm(forms.Form):
    """
    Form for quickly adding a product to inventory from product detail page.
    """
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label=_('Quantity'),
        widget=forms.NumberInput(attrs={'min': 1})
    )
    price = forms.DecimalField(
        min_value=Decimal('0.01'),
        max_digits=10,
        decimal_places=2,
        label=_('Price'),
        widget=forms.NumberInput(attrs={'min': 0.01, 'step': 0.01})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        product_id = cleaned_data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                cleaned_data['product'] = product
            except Product.DoesNotExist:
                self.add_error('product_id', _('Product does not exist.'))
                
        return cleaned_data


class FulfillOrderItemForm(forms.Form):
    """
    Form for fulfilling an order item.
    """
    order_item_id = forms.IntegerField(widget=forms.HiddenInput())
    confirm = forms.BooleanField(
        required=True,
        label=_('I confirm this item has been shipped/fulfilled')
    )
