from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.db.models import Q, Avg, Count
from django.utils.translation import gettext_lazy as _

from .models import Product, Category
from .forms import ProductForm, ProductSearchForm


class ProductListView(ListView):
    """
    View for listing all products, with optional category filtering.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Category filtering
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Add category info if filtering by category
        category_id = self.kwargs.get('category_id')
        if category_id:
            context['current_category'] = get_object_or_404(Category, pk=category_id)
            
        return context


class ProductDetailView(DetailView):
    """
    View for displaying detailed product information.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add reviews and seller information to context
        product = self.get_object()
        context['reviews'] = product.reviews.all().order_by('-created_at')
        context['inventories'] = product.inventory_items.filter(quantity__gt=0).select_related('seller')
        
        # Add similar products
        context['similar_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:5]
        
        # Check if user has already reviewed this product
        if self.request.user.is_authenticated:
            context['user_review'] = product.reviews.filter(user=self.request.user).first()
            
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new product.
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _('Product created successfully!'))
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing product.
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'
    
    def test_func(self):
        """
        Only the creator of the product can update it.
        """
        product = self.get_object()
        return self.request.user == product.created_by
    
    def form_valid(self, form):
        messages.success(self.request, _('Product updated successfully!'))
        return super().form_valid(form)


class ProductSearchView(FormView):
    """
    View for searching products with various filters.
    """
    template_name = 'products/product_search.html'
    form_class = ProductSearchForm
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-populate form with query parameters
        for field in self.form_class.base_fields:
            if field in self.request.GET:
                initial[field] = self.request.GET.get(field)
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Only perform search if there are query parameters
        if self.request.GET:
            # Get form parameters
            query = self.request.GET.get('query', '')
            category_id = self.request.GET.get('category', '')
            min_price = self.request.GET.get('min_price', '')
            max_price = self.request.GET.get('max_price', '')
            sort_by = self.request.GET.get('sort_by', '-created_at')
            
            # Start with all products
            products = Product.objects.all()
            
            # Apply filters
            if query:
                products = products.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                )
            
            if category_id:
                products = products.filter(category_id=category_id)
            
            if min_price:
                products = products.filter(inventory__price__gte=min_price)
            
            if max_price:
                products = products.filter(inventory__price__lte=max_price)
            
            # Apply sorting
            if sort_by == 'price_asc':
                products = products.annotate(min_inv_price=Avg('inventory__price')).order_by('min_inv_price')
            elif sort_by == 'price_desc':
                products = products.annotate(min_inv_price=Avg('inventory__price')).order_by('-min_inv_price')
            else:
                products = products.order_by(sort_by)
            
            # Remove duplicates
            products = products.distinct()
            
            context['products'] = products
            context['search_performed'] = True
        
        context['categories'] = Category.objects.all()
        return context


def category_list(request):
    """
    View for displaying all categories.
    """
    # Get all categories and create a list of dictionaries with category and product count
    categories = []
    for category in Category.objects.all():
        categories.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at,
            'product_count': category.product_set.count(),
            'get_absolute_url': category.get_absolute_url()
        })
    
    return render(request, 'products/category_list.html', {
        'categories': categories
    })
