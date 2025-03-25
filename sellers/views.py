from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Sum, Count, F
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.http import JsonResponse

from .models import Inventory
from .forms import InventoryForm, QuickAddInventoryForm, FulfillOrderItemForm
from carts.models import OrderItem, Order


class InventoryListView(LoginRequiredMixin, ListView):
    """
    View for listing a seller's inventory.
    """
    model = Inventory
    template_name = 'sellers/inventory_list.html'
    context_object_name = 'inventory_items'
    paginate_by = 20
    
    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user).select_related('product')


class InventoryCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new inventory item.
    """
    model = Inventory
    form_class = InventoryForm
    template_name = 'sellers/inventory_form.html'
    success_url = reverse_lazy('sellers:inventory')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['seller'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, _('Product added to your inventory successfully.'))
        return super().form_valid(form)


class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing inventory item.
    """
    model = Inventory
    form_class = InventoryForm
    template_name = 'sellers/inventory_form.html'
    success_url = reverse_lazy('sellers:inventory')
    
    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['seller'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, _('Inventory updated successfully.'))
        return super().form_valid(form)


class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for removing a product from inventory.
    """
    model = Inventory
    template_name = 'sellers/inventory_confirm_delete.html'
    success_url = reverse_lazy('sellers:inventory')
    
    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Product removed from your inventory.'))
        return super().delete(request, *args, **kwargs)


@login_required
def quick_add_to_inventory(request):
    """
    View for quickly adding a product to inventory from product detail page.
    """
    if request.method == 'POST':
        form = QuickAddInventoryForm(request.POST)
        
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            
            # Check if the product is already in inventory
            inventory, created = Inventory.objects.get_or_create(
                seller=request.user,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price': price
                }
            )
            
            if not created:
                # Update existing inventory
                inventory.quantity += quantity
                inventory.price = price  # Update to new price
                inventory.save()
                messages.success(
                    request,
                    _('Updated %(product)s in your inventory.') %
                    {'product': product.name}
                )
            else:
                messages.success(
                    request,
                    _('Added %(product)s to your inventory.') %
                    {'product': product.name}
                )
                
            return redirect('products:detail', pk=product.id)
        else:
            messages.error(request, _('Error adding to inventory.'))
            return redirect('products:list')
    
    return redirect('products:list')


class OrderFulfillmentListView(LoginRequiredMixin, ListView):
    """
    View for listing orders that need fulfillment by the seller.
    """
    template_name = 'sellers/order_fulfillment_list.html'
    context_object_name = 'order_items'
    paginate_by = 20
    
    def get_queryset(self):
        # Get all order items for products in the seller's inventory
        return OrderItem.objects.filter(
            inventory__seller=self.request.user
        ).select_related(
            'order__user', 'inventory__product'
        ).order_by('-order__created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter for pending items
        pending_only = self.request.GET.get('pending', False)
        if pending_only:
            context['order_items'] = context['order_items'].filter(is_fulfilled=False)
            context['pending_only'] = True
            
        # Add counts for fulfilled/unfulfilled
        context['unfulfilled_count'] = OrderItem.objects.filter(
            inventory__seller=self.request.user,
            is_fulfilled=False
        ).count()
        
        context['fulfilled_count'] = OrderItem.objects.filter(
            inventory__seller=self.request.user,
            is_fulfilled=True
        ).count()
        
        return context


@login_required
def fulfill_order_item(request, item_id):
    """
    View for marking an order item as fulfilled.
    """
    order_item = get_object_or_404(
        OrderItem,
        id=item_id,
        inventory__seller=request.user,
        is_fulfilled=False
    )
    
    if request.method == 'POST':
        form = FulfillOrderItemForm(request.POST)
        
        if form.is_valid() and int(form.cleaned_data['order_item_id']) == order_item.id:
            # Mark as fulfilled
            order_item.is_fulfilled = True
            order_item.fulfilled_at = timezone.now()
            order_item.save()
            
            # Update order status if all items are fulfilled
            order = order_item.order
            if not OrderItem.objects.filter(order=order, is_fulfilled=False).exists():
                order.is_fulfilled = True
                order.status = 'fulfilled'
                order.save()
            elif order.status == 'pending':
                order.status = 'processing'
                order.save()
                
            messages.success(request, _('Order item marked as fulfilled.'))
        else:
            messages.error(request, _('Error fulfilling order item.'))
    
    return redirect('sellers:order_fulfillment')


class SalesAnalyticsView(LoginRequiredMixin, ListView):
    """
    View for displaying sales analytics for a seller.
    """
    template_name = 'sellers/sales_analytics.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        # Get products with sales statistics
        return Inventory.objects.filter(
            seller=self.request.user
        ).values(
            'product__name'
        ).annotate(
            total_sales=Sum(F('order_items__quantity') * F('order_items__unit_price')),
            units_sold=Sum('order_items__quantity'),
            order_count=Count('order_items__order', distinct=True)
        ).order_by('-total_sales')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add total sales amount
        context['total_sales'] = OrderItem.objects.filter(
            inventory__seller=self.request.user
        ).aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total'] or 0
        
        # Add total units sold
        context['total_units'] = OrderItem.objects.filter(
            inventory__seller=self.request.user
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        # Add total orders fulfilled
        context['orders_fulfilled'] = OrderItem.objects.filter(
            inventory__seller=self.request.user,
            is_fulfilled=True
        ).values('order').distinct().count()
        
        # Add total orders pending
        context['orders_pending'] = OrderItem.objects.filter(
            inventory__seller=self.request.user,
            is_fulfilled=False
        ).values('order').distinct().count()
        
        return context
