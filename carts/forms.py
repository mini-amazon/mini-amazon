from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CartItem, Order


class CartItemForm(forms.ModelForm):
    """
    Form for adding or updating a cart item.
    """
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control',
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError(_('Quantity must be at least 1.'))
            
        # Check if inventory has enough stock
        if self.instance.pk:
            inventory = self.instance.inventory
            if inventory.quantity < quantity:
                raise forms.ValidationError(
                    _('Only %(count)d items available in stock.') % {'count': inventory.quantity}
                )
                
        return quantity


class AddToCartForm(forms.Form):
    """
    Form for adding a product to cart.
    """
    inventory_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
        })
    )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError(_('Quantity must be at least 1.'))
        return quantity


class CheckoutForm(forms.Form):
    """
    Form for proceeding to checkout.
    """
    confirm = forms.BooleanField(
        required=True,
        initial=False,
        label=_('I confirm my order details are correct')
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        """
        验证表单数据，进行库存和余额检查
        """
        cleaned_data = super().clean()
        
        # 确保我们有用户和购物车对象
        if self.user and self.cart:
            # 验证余额充足
            cart_total = self.cart.total
            user_balance = self.user.balance
            
            if user_balance < cart_total:
                self.add_error(None, 
                               _('Your balance of %(balance)s is insufficient for this order (%(total)s).') % 
                               {'balance': user_balance, 'total': cart_total})
                
            # 验证库存可用性
            for item in self.cart.items.all():
                if item.inventory.quantity < item.quantity:
                    self.add_error(
                        None, 
                        _('Not enough stock for %(product)s (Only %(available)d available).') % 
                        {'product': item.inventory.product.name, 'available': item.inventory.quantity}
                    )
        
        return cleaned_data
