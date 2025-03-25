from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from .models import ProductReview, SellerReview, Message
from .forms import ProductReviewForm, SellerReviewForm, MessageForm
from products.models import Product
from users.models import User
from carts.models import Order


@login_required
def create_product_review(request, product_id):
    """
    View for creating or updating a product review.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if user has already reviewed this product
    review = ProductReview.objects.filter(user=request.user, product=product).first()
    
    if request.method == 'POST':
        form = ProductReviewForm(
            request.POST,
            instance=review,
            user=request.user,
            product=product
        )
        
        if form.is_valid():
            form.save()
            messages.success(request, _('Your review has been saved.'))
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductReviewForm(
            instance=review,
            user=request.user,
            product=product
        )
    
    return render(request, 'social/product_review_form.html', {
        'form': form,
        'product': product,
        'is_update': review is not None
    })


@login_required
def delete_product_review(request, review_id):
    """
    View for deleting a product review.
    """
    review = get_object_or_404(ProductReview, pk=review_id, user=request.user)
    product = review.product
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, _('Your review has been deleted.'))
        return redirect('products:detail', pk=product.pk)
    
    return render(request, 'social/product_review_confirm_delete.html', {
        'review': review,
        'product': product
    })


@login_required
def create_seller_review(request, seller_id):
    """
    View for creating or updating a seller review.
    """
    seller = get_object_or_404(User, pk=seller_id)
    
    # Don't allow self-review
    if seller == request.user:
        messages.error(request, _('You cannot review yourself.'))
        return redirect('users:public_profile', pk=seller.pk)
    
    # Check if there's an existing review for any order with this seller
    review = SellerReview.objects.filter(user=request.user, seller=seller).first()
    
    if request.method == 'POST':
        form = SellerReviewForm(
            request.POST,
            instance=review,
            user=request.user,
            seller=seller
        )
        
        if form.is_valid():
            form.save()
            messages.success(request, _('Your review has been saved.'))
            return redirect('users:public_profile', pk=seller.pk)
    else:
        form = SellerReviewForm(
            instance=review,
            user=request.user,
            seller=seller
        )
    
    return render(request, 'social/seller_review_form.html', {
        'form': form,
        'seller': seller,
        'is_update': review is not None
    })


@login_required
def delete_seller_review(request, review_id):
    """
    View for deleting a seller review.
    """
    review = get_object_or_404(SellerReview, pk=review_id, user=request.user)
    seller = review.seller
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, _('Your review has been deleted.'))
        return redirect('users:public_profile', pk=seller.pk)
    
    return render(request, 'social/seller_review_confirm_delete.html', {
        'review': review,
        'seller': seller
    })


class UserReviewListView(LoginRequiredMixin, ListView):
    """
    View for listing all reviews written by the user.
    """
    template_name = 'social/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        # Combine product reviews and seller reviews
        product_reviews = ProductReview.objects.filter(user=self.request.user)
        seller_reviews = SellerReview.objects.filter(user=self.request.user)
        
        sort_by = self.request.GET.get('sort_by', '-created_at')
        
        # Use different sorting based on request parameter
        if sort_by == 'product':
            product_reviews = product_reviews.order_by('product__name')
            seller_reviews = seller_reviews.order_by('seller__full_name')
        elif sort_by == 'rating':
            product_reviews = product_reviews.order_by('-rating')
            seller_reviews = seller_reviews.order_by('-rating')
        else:  # Default to created_at
            product_reviews = product_reviews.order_by('-created_at')
            seller_reviews = seller_reviews.order_by('-created_at')
        
        # Convert to lists and combine
        product_reviews = list(product_reviews)
        seller_reviews = list(seller_reviews)
        
        # Add type attribute to distinguish between review types
        for review in product_reviews:
            review.type = 'product'
        for review in seller_reviews:
            review.type = 'seller'
        
        # Combine and sort
        combined_reviews = product_reviews + seller_reviews
        
        if sort_by == 'product':
            combined_reviews.sort(key=lambda x: (x.product.name if hasattr(x, 'product') else x.seller.full_name))
        elif sort_by == 'rating':
            combined_reviews.sort(key=lambda x: x.rating, reverse=True)
        else:  # Default to created_at
            combined_reviews.sort(key=lambda x: x.created_at, reverse=True)
            
        return combined_reviews
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', '-created_at')
        return context


@login_required
def conversation_list(request):
    """
    View for listing all conversations for the current user.
    """
    # Get all users the current user has exchanged messages with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    
    # Combine and remove duplicates
    conversation_user_ids = set(list(sent_to) + list(received_from))
    
    # Get the actual user objects
    conversation_users = User.objects.filter(id__in=conversation_user_ids)
    
    # Get the latest message for each conversation
    conversations = []
    for user in conversation_users:
        latest_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
        ).order_by('-created_at').first()
        
        if latest_message:
            conversations.append({
                'user': user,
                'latest_message': latest_message,
                'unread_count': Message.objects.filter(sender=user, receiver=request.user, is_read=False).count()
            })
    
    # Sort by latest message first
    conversations.sort(key=lambda x: x['latest_message'].created_at, reverse=True)
    
    return render(request, 'social/conversation_list.html', {
        'conversations': conversations
    })


@login_required
def conversation_detail(request, user_id):
    """
    View for displaying a conversation with another user.
    """
    other_user = get_object_or_404(User, pk=user_id)
    
    # Get all messages between the two users
    messages_queryset = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    
    # Mark unread messages as read
    messages_queryset.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    # Get orders involving both users (for context)
    orders = Order.objects.filter(
        Q(user=request.user, items__inventory__seller=other_user) | 
        Q(user=other_user, items__inventory__seller=request.user)
    ).distinct()
    
    # Handle new message form
    if request.method == 'POST':
        form = MessageForm(
            request.POST,
            sender=request.user,
            receiver=other_user
        )
        
        if form.is_valid():
            message = form.save()
            
            # If AJAX request, return the message as JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'content': message.content,
                        'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
                        'is_sender': True
                    }
                })
            
            # Redirect to the conversation page
            return redirect('social:conversation', user_id=user_id)
    else:
        form = MessageForm(
            sender=request.user,
            receiver=other_user
        )
    
    return render(request, 'social/conversation_detail.html', {
        'messages_list': messages_queryset,
        'other_user': other_user,
        'form': form,
        'orders': orders
    })
