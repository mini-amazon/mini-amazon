from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Inventory
from .forms import InventoryForm, QuickAddInventoryForm, FulfillOrderItemForm
from products.models import Product, Category
from carts.models import Order, OrderItem

User = get_user_model()


class InventoryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='seller@example.com',
            password='testpassword123',
            full_name='Test Seller',
            address='123 Seller St'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.inventory = Inventory.objects.create(
            seller=self.user,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )

    def test_inventory_creation(self):
        """Test that an inventory item can be created with the correct fields"""
        self.assertEqual(self.inventory.seller, self.user)
        self.assertEqual(self.inventory.product, self.product)
        self.assertEqual(self.inventory.quantity, 10)
        self.assertEqual(self.inventory.price, Decimal('25.00'))
        self.assertIsNotNone(self.inventory.created_at)
        self.assertIsNotNone(self.inventory.updated_at)

    def test_inventory_string_representation(self):
        """Test the string representation of an inventory item"""
        self.assertEqual(str(self.inventory), "Test Product (10 @ $25.00)")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(self.inventory.get_absolute_url(), reverse('sellers:inventory'))

    def test_is_in_stock(self):
        """Test is_in_stock property"""
        self.assertTrue(self.inventory.is_in_stock)
        
        # Update quantity to 0
        self.inventory.quantity = 0
        self.inventory.save()
        
        self.assertFalse(self.inventory.is_in_stock)

    def test_total_value(self):
        """Test total_value property"""
        self.assertEqual(self.inventory.total_value, Decimal('250.00'))  # 10 * 25.00


class InventoryFormTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            email='seller@example.com',
            password='testpassword123',
            full_name='Test Seller',
            address='123 Seller St'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.seller
        )

    def test_inventory_form_valid_data(self):
        """Test inventory form with valid data"""
        form = InventoryForm({
            'product': self.product.id,
            'quantity': 10,
            'price': '25.00'
        }, seller=self.seller)
        self.assertTrue(form.is_valid())

    def test_inventory_form_negative_quantity(self):
        """Test inventory form with negative quantity"""
        form = InventoryForm({
            'product': self.product.id,
            'quantity': -1,  # Negative quantity
            'price': '25.00'
        }, seller=self.seller)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_inventory_form_negative_price(self):
        """Test inventory form with negative price"""
        form = InventoryForm({
            'product': self.product.id,
            'quantity': 10,
            'price': '-1.00'  # Negative price
        }, seller=self.seller)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_inventory_form_duplicate_product(self):
        """Test inventory form with duplicate product"""
        # Create an existing inventory item
        Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=5,
            price='20.00'
        )
        
        # Try to create another one for the same product
        form = InventoryForm({
            'product': self.product.id,
            'quantity': 10,
            'price': '25.00'
        }, seller=self.seller)
        self.assertFalse(form.is_valid())
        self.assertIn('product', form.errors)

    def test_quick_add_inventory_form_valid_data(self):
        """Test quick add inventory form with valid data"""
        form = QuickAddInventoryForm({
            'product_id': self.product.id,
            'quantity': 10,
            'price': '25.00'
        })
        self.assertTrue(form.is_valid())

    def test_quick_add_inventory_form_invalid_product(self):
        """Test quick add inventory form with invalid product ID"""
        form = QuickAddInventoryForm({
            'product_id': 9999,  # Non-existent product ID
            'quantity': 10,
            'price': '25.00'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('product_id', form.errors)

    def test_fulfill_order_item_form_valid_data(self):
        """Test fulfill order item form with valid data"""
        form = FulfillOrderItemForm({
            'order_item_id': 1,
            'confirm': True
        })
        self.assertTrue(form.is_valid())

    def test_fulfill_order_item_form_no_confirmation(self):
        """Test fulfill order item form without confirmation"""
        form = FulfillOrderItemForm({
            'order_item_id': 1,
            'confirm': False  # Not confirmed
        })
        self.assertFalse(form.is_valid())
        self.assertIn('confirm', form.errors)


class SellerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller = User.objects.create_user(
            email='seller@example.com',
            password='testpassword123',
            full_name='Test Seller',
            address='123 Seller St'
        )
        self.client.login(email='seller@example.com', password='testpassword123')
        
        self.buyer = User.objects.create_user(
            email='buyer@example.com',
            password='testpassword123',
            full_name='Test Buyer',
            address='123 Buyer St'
        )
        
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.seller
        )
        
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Create an order with order item
        self.order = Order.objects.create(
            user=self.buyer,
            total_amount=Decimal('50.00'),
            status='pending',
            is_fulfilled=False
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=False
        )

    def test_inventory_list_view(self):
        """Test inventory list view"""
        response = self.client.get(reverse('sellers:inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/inventory_list.html')
        self.assertContains(response, 'Test Product')

    def test_inventory_create_view(self):
        """Test inventory create view"""
        # Create another product
        product2 = Product.objects.create(
            name='Test Product 2',
            description='Another Test Description',
            category=self.category,
            created_by=self.seller
        )
        
        response = self.client.get(reverse('sellers:inventory_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/inventory_form.html')
        
        # Test creating a new inventory item
        response = self.client.post(reverse('sellers:inventory_create'), {
            'product': product2.id,
            'quantity': 5,
            'price': '30.00'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if inventory was created
        self.assertTrue(Inventory.objects.filter(product=product2).exists())
        new_inventory = Inventory.objects.get(product=product2)
        self.assertEqual(new_inventory.quantity, 5)
        self.assertEqual(new_inventory.price, Decimal('30.00'))

    def test_inventory_update_view(self):
        """Test inventory update view"""
        response = self.client.get(reverse('sellers:inventory_update', kwargs={'pk': self.inventory.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/inventory_form.html')
        
        # Test updating inventory
        response = self.client.post(reverse('sellers:inventory_update', kwargs={'pk': self.inventory.pk}), {
            'product': self.product.id,
            'quantity': 15,
            'price': '35.00'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if inventory was updated
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 15)
        self.assertEqual(self.inventory.price, Decimal('35.00'))

    def test_inventory_delete_view(self):
        """Test inventory delete view"""
        response = self.client.get(reverse('sellers:inventory_delete', kwargs={'pk': self.inventory.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/inventory_confirm_delete.html')
        
        # Test deleting inventory
        response = self.client.post(reverse('sellers:inventory_delete', kwargs={'pk': self.inventory.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if inventory was deleted
        self.assertFalse(Inventory.objects.filter(pk=self.inventory.pk).exists())

    def test_quick_add_to_inventory(self):
        """Test quick add to inventory view"""
        # Create another product
        product2 = Product.objects.create(
            name='Test Product 2',
            description='Another Test Description',
            category=self.category,
            created_by=self.seller
        )
        
        response = self.client.post(reverse('sellers:quick_add_inventory'), {
            'product_id': product2.id,
            'quantity': 5,
            'price': '30.00'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if inventory was created
        self.assertTrue(Inventory.objects.filter(product=product2).exists())
        new_inventory = Inventory.objects.get(product=product2)
        self.assertEqual(new_inventory.quantity, 5)
        self.assertEqual(new_inventory.price, Decimal('30.00'))

    def test_order_fulfillment_list_view(self):
        """Test order fulfillment list view"""
        response = self.client.get(reverse('sellers:order_fulfillment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/order_fulfillment_list.html')
        self.assertContains(response, 'Test Product')

    def test_fulfill_order_item(self):
        """Test fulfill order item view"""
        response = self.client.post(reverse('sellers:fulfill_order_item', kwargs={'item_id': self.order_item.pk}), {
            'order_item_id': self.order_item.pk,
            'confirm': True
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if order item was marked as fulfilled
        self.order_item.refresh_from_db()
        self.assertTrue(self.order_item.is_fulfilled)
        self.assertIsNotNone(self.order_item.fulfilled_at)
        
        # Check if order status was updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'fulfilled')
        self.assertTrue(self.order.is_fulfilled)

    def test_sales_analytics_view(self):
        """Test sales analytics view"""
        response = self.client.get(reverse('sellers:sales_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellers/sales_analytics.html')
        
        # Should contain product name
        self.assertContains(response, 'Test Product')
        
        # Check context data
        self.assertEqual(response.context['total_units'], 2)  # 2 units sold
        self.assertEqual(response.context['total_sales'], Decimal('50.00'))  # 2 * 25.00
