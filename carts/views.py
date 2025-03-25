from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal

from .models import Cart, CartItem, Order, OrderItem
from .forms import CartItemForm, AddToCartForm, CheckoutForm
from sellers.models import Inventory


@login_required
def cart_view(request):
    """
    View for displaying the user's shopping cart.
    """
    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get cart items with related inventory and product
    cart_items = cart.items.select_related('inventory__product').all()
    
    return render(request, 'carts/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
def add_to_cart(request):
    """
    View for adding an item to the shopping cart.
    """
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        
        if form.is_valid():
            inventory_id = form.cleaned_data['inventory_id']
            quantity = form.cleaned_data['quantity']
            
            # Get inventory
            try:
                inventory = Inventory.objects.get(id=inventory_id)
                
                # Check if inventory has enough stock
                if inventory.quantity < quantity:
                    messages.error(
                        request, 
                        _('Only %(count)d items available in stock.') % 
                        {'count': inventory.quantity}
                    )
                    return redirect('products:detail', pk=inventory.product.id)
                    
                # Get or create user's cart
                cart, created = Cart.objects.get_or_create(user=request.user)
                
                # Get or create cart item
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    inventory=inventory,
                    defaults={'quantity': quantity}
                )
                
                # Update quantity if item already exists
                if not created:
                    cart_item.quantity += quantity
                    
                    # Validate against available stock
                    if cart_item.quantity > inventory.quantity:
                        cart_item.quantity = inventory.quantity
                        messages.warning(
                            request,
                            _('Quantity adjusted to available stock (%(count)d).') %
                            {'count': inventory.quantity}
                        )
                        
                    cart_item.save()
                
                messages.success(
                    request,
                    _('%(product)s added to your cart.') %
                    {'product': inventory.product.name}
                )
                
            except Inventory.DoesNotExist:
                messages.error(request, _('Product not found.'))
                
        else:
            messages.error(request, _('Invalid form submission.'))
            
    return redirect('carts:view')


@login_required
def update_cart_item(request, item_id):
    """
    View for updating the quantity of a cart item.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        
        if form.is_valid():
            # If quantity is 0, remove the item
            if form.cleaned_data['quantity'] == 0:
                cart_item.delete()
                message = _('Item removed from cart.')
                success = True
            else:
                form.save()
                message = _('Cart updated.')
                success = True
        else:
            message = form.errors.get('quantity', _('Error updating cart.'))
            success = False
        
        # 检查是否为AJAX请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': str(message),
                'cart_total': float(request.user.cart.total),
                'item_quantity': cart_item.quantity if success and cart_item.id else 0,
                'item_subtotal': float(cart_item.subtotal) if success and cart_item.id else 0
            })
        
        # 非AJAX请求的处理
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
            
    return redirect('carts:view')


@login_required
def remove_from_cart(request, item_id):
    """
    View for removing an item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.inventory.product.name
    
    cart_item.delete()
    messages.success(
        request,
        _('%(product)s removed from your cart.') %
        {'product': product_name}
    )
    
    return redirect('carts:view')


@login_required
def checkout(request):
    """
    View for the checkout process.
    """
    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if cart.items.count() == 0:
        messages.warning(request, _('Your cart is empty.'))
        return redirect('carts:view')
        
    if request.method == 'POST':
        form = CheckoutForm(
            request.POST,
            user=request.user,
            cart=cart
        )
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=cart.total,
                        status='pending',
                        is_fulfilled=False
                    )
                    
                    # Create order items and update inventory
                    for cart_item in cart.items.all():
                        inventory = cart_item.inventory
                        
                        # Verify inventory before finalizing
                        if inventory.quantity < cart_item.quantity:
                            raise ValueError(
                                _('Not enough stock for %(product)s.') %
                                {'product': inventory.product.name}
                            )
                            
                        # Create order item
                        OrderItem.objects.create(
                            order=order,
                            inventory=inventory,
                            quantity=cart_item.quantity,
                            unit_price=inventory.price,
                            is_fulfilled=False
                        )
                        
                        # Update inventory
                        inventory.quantity -= cart_item.quantity
                        inventory.save()
                        
                        # Update seller balance
                        seller = inventory.seller
                        seller.add_to_balance(cart_item.quantity * inventory.price)
                    
                    # Update buyer balance
                    request.user.withdraw_from_balance(order.total_amount)
                    
                    # Clear cart
                    cart.clear()
                    
                    messages.success(
                        request,
                        _('Order placed successfully!')
                    )
                    
                    return redirect('carts:order_detail', pk=order.id)
                    
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('carts:checkout')
                
            except Exception as e:
                messages.error(
                    request,
                    _('Error processing your order: %(error)s') %
                    {'error': str(e)}
                )
                return redirect('carts:checkout')
        else:
            # 表单验证失败，显示错误信息
            for error in form.non_field_errors():
                messages.error(request, error)
            
            # 不要在这里访问 form.cleaned_data
    else:
        form = CheckoutForm(
            user=request.user,
            cart=cart
        )
    
    # 计算购物车总价和结账后的余额
    cart_total = cart.total
    remaining_balance = request.user.balance - cart_total
    
    # Debug: 打印变量内容以便于调试
    print(f"DEBUG: cart_total = {cart_total}, type = {type(cart_total)}")
    print(f"DEBUG: remaining_balance = {remaining_balance}, type = {type(remaining_balance)}")
    print(f"DEBUG: user.balance = {request.user.balance}, type = {type(request.user.balance)}")
    
    # 确保我们传递的是数值类型, 并确保是Decimal格式
    if cart_total is None:
        cart_total = Decimal('0.00')
    else:
        # 确保是Decimal，并格式化为两位小数
        cart_total = Decimal(str(cart_total)).quantize(Decimal('0.01'))
    
    # 处理remaining_balance，确保不会是None
    if remaining_balance is None:
        remaining_balance = request.user.balance
    else:
        remaining_balance = Decimal(str(remaining_balance)).quantize(Decimal('0.01'))
    
    return render(request, 'carts/checkout.html', {
        'form': form,
        'cart': cart,
        'cart_items': cart.items.select_related('inventory__product').all(),
        'cart_total': cart_total,
        'remaining_balance': remaining_balance
    })


class OrderListView(LoginRequiredMixin, ListView):
    """
    View for listing a user's orders.
    """
    model = Order
    template_name = 'carts/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying the details of an order.
    """
    model = Order
    template_name = 'carts/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        # Ensure users can only see their own orders
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__inventory__product',
            'items__inventory__seller'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data needed for the template
        return context


@login_required
def cancel_order(request, pk):
    """
    View for cancelling an order.
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    # Can only cancel pending orders
    if order.status != 'pending':
        messages.error(
            request,
            _('Cannot cancel orders that are already being processed or fulfilled.')
        )
        return redirect('carts:order_detail', pk=order.pk)
        
    try:
        with transaction.atomic():
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            # Refund buyer
            request.user.add_to_balance(order.total_amount)
            
            # Update inventory and seller balances
            for item in order.items.all():
                # Restore inventory
                inventory = item.inventory
                inventory.quantity += item.quantity
                inventory.save()
                
                # Deduct from seller balance
                seller = inventory.seller
                seller.withdraw_from_balance(item.quantity * item.unit_price)
                
            messages.success(request, _('Order cancelled successfully.'))
            
    except Exception as e:
        messages.error(
            request,
            _('Error cancelling order: %(error)s') %
            {'error': str(e)}
        )
        
    return redirect('carts:order_detail', pk=order.pk)


@login_required
def update_cart_item_api(request, item_id):
    """
    API view for updating cart item quantity via AJAX.
    """
    if request.method == 'POST' and request.is_ajax():
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', 0))
            
            if quantity <= 0:
                # Remove item
                cart_item.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': _('Item removed from cart.'),
                    'deleted': True,
                    'cart_total': cart_item.cart.total
                })
                
            # Check available inventory
            if quantity > cart_item.inventory.quantity:
                return JsonResponse({
                    'status': 'error',
                    'message': _('Only %(count)d items available in stock.') % 
                               {'count': cart_item.inventory.quantity}
                })
            
            # Update quantity
            cart_item.quantity = quantity
            cart_item.save()
            
            # Calculate item subtotal and cart total
            item_subtotal = cart_item.subtotal
            cart_total = cart_item.cart.total
            
            return JsonResponse({
                'status': 'success',
                'message': _('Cart updated.'),
                'item_subtotal': float(item_subtotal),
                'cart_total': float(cart_total)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': _('Invalid request.')
    })


@login_required
def update_cart(request):
    """
    View for updating the entire cart.
    """
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Process cart updates
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                try:
                    # Extract cart item ID from the field name
                    item_id = int(key.split('_')[1])
                    quantity = int(value)
                    
                    # Get cart item
                    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
                    
                    # Update or delete based on quantity
                    if quantity <= 0:
                        cart_item.delete()
                    else:
                        # Check inventory
                        if quantity > cart_item.inventory.quantity:
                            messages.warning(
                                request, 
                                _('Only %(count)d items available for %(product)s.') % 
                                {'count': cart_item.inventory.quantity, 'product': cart_item.inventory.product.name}
                            )
                            quantity = cart_item.inventory.quantity
                            
                        cart_item.quantity = quantity
                        cart_item.save()
                        
                except (ValueError, CartItem.DoesNotExist):
                    continue
                    
        messages.success(request, _('Cart updated successfully.'))
        
    return redirect('carts:view')


@login_required
def place_order(request):
    """
    View for placing an order.
    """
    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if cart.items.count() == 0:
        messages.warning(request, _('Your cart is empty.'))
        return redirect('carts:view')
        
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Check if user has enough balance
                if request.user.balance < cart.total:
                    messages.error(
                        request,
                        _('Insufficient balance. Please add funds to your account.')
                    )
                    return redirect('carts:checkout')
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total,
                    status='pending',
                    is_fulfilled=False
                )
                
                # Create order items and update inventory
                for cart_item in cart.items.all():
                    inventory = cart_item.inventory
                    
                    # Verify inventory before finalizing
                    if inventory.quantity < cart_item.quantity:
                        raise ValueError(
                            _('Not enough stock for %(product)s.') %
                            {'product': inventory.product.name}
                        )
                        
                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        inventory=inventory,
                        quantity=cart_item.quantity,
                        unit_price=inventory.price,
                        is_fulfilled=False
                    )
                    
                    # Update inventory
                    inventory.quantity -= cart_item.quantity
                    inventory.save()
                    
                    # Update seller balance
                    seller = inventory.seller
                    seller.add_to_balance(cart_item.quantity * inventory.price)
                
                # Update buyer balance
                request.user.withdraw_from_balance(order.total_amount)
                
                # Clear cart
                cart.clear()
                
                messages.success(
                    request,
                    _('Order placed successfully!')
                )
                
                return redirect('carts:order_detail', pk=order.id)
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('carts:checkout')
            
        except Exception as e:
            messages.error(
                request,
                _('Error processing your order: %(error)s') %
                {'error': str(e)}
            )
            return redirect('carts:checkout')
    
    # GET requests should go to checkout page
    return redirect('carts:checkout')


@login_required
def clear_cart(request):
    """
    View for clearing all items from the cart.
    """
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.clear()
        messages.success(request, _('Cart has been emptied.'))
        
    return redirect('carts:view')
