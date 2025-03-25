from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Cart, CartItem, Order, OrderItem
from .forms import CartItemForm, AddToCartForm, CheckoutForm
from products.models import Product, Category
from sellers.models import Inventory

User = get_user_model()


class CartModelTests(TransactionTestCase):
    def setUp(self):
        # Using unique email addresses for each test method to prevent conflicts
        test_name = self._testMethodName
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        """Test that a cart can be created with the correct fields"""
        self.assertEqual(self.cart.user, self.user)
        self.assertIsNotNone(self.cart.created_at)
        self.assertIsNotNone(self.cart.updated_at)

    def test_cart_string_representation(self):
        """Test the string representation of a cart"""
        self.assertEqual(str(self.cart), f"{self.user.email}'s Cart")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(self.cart.get_absolute_url(), reverse('carts:view'))

    def test_total_empty_cart(self):
        """Test total property with an empty cart"""
        self.assertEqual(self.cart.total, Decimal('0'))

    def test_item_count(self):
        """Test item_count property"""
        self.assertEqual(self.cart.item_count, 0)

    def test_clear(self):
        """Test clear method"""
        # Create product, seller, inventory
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=category,
            created_by=self.user
        )
        seller = User.objects.create_user(
            email=f'seller_{self._testMethodName}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        inventory = Inventory.objects.create(
            seller=seller,
            product=product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Add item to cart
        cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=inventory,
            quantity=2
        )
        
        self.assertEqual(self.cart.item_count, 1)
        
        # Clear cart
        self.cart.clear()
        
        self.assertEqual(self.cart.item_count, 0)


class CartItemModelTests(TransactionTestCase):
    def setUp(self):
        test_name = self._testMethodName
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        self.cart = Cart.objects.create(user=self.user)
        
        # Create product, seller, inventory
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.seller = User.objects.create_user(
            email=f'seller_{test_name}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=self.inventory,
            quantity=2
        )

    def test_cart_item_creation(self):
        """Test that a cart item can be created with the correct fields"""
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.inventory, self.inventory)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertIsNotNone(self.cart_item.created_at)
        self.assertIsNotNone(self.cart_item.updated_at)

    def test_cart_item_string_representation(self):
        """Test the string representation of a cart item"""
        self.assertEqual(str(self.cart_item), "2 x Test Product")

    def test_subtotal(self):
        """Test subtotal property"""
        self.assertEqual(self.cart_item.subtotal, Decimal('50.00'))  # 2 * 25.00


class OrderModelTests(TransactionTestCase):
    def setUp(self):
        test_name = self._testMethodName
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('100.00'),
            status='pending',
            is_fulfilled=False
        )

    def test_order_creation(self):
        """Test that an order can be created with the correct fields"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_amount, Decimal('100.00'))
        self.assertEqual(self.order.status, 'pending')
        self.assertFalse(self.order.is_fulfilled)
        self.assertIsNotNone(self.order.created_at)
        self.assertIsNotNone(self.order.updated_at)

    def test_order_string_representation(self):
        """Test the string representation of an order"""
        self.assertEqual(str(self.order), f"Order #{self.order.id} - {self.user.email}")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.order.get_absolute_url(),
            reverse('carts:order_detail', kwargs={'pk': self.order.pk})
        )

    def test_update_status(self):
        """Test update_status method"""
        # Create items for the order
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=category,
            created_by=self.user
        )
        seller = User.objects.create_user(
            email=f'seller_{self._testMethodName}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        inventory = Inventory.objects.create(
            seller=seller,
            product=product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Create order items
        order_item1 = OrderItem.objects.create(
            order=self.order,
            inventory=inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=True
        )
        
        order_item2 = OrderItem.objects.create(
            order=self.order,
            inventory=inventory,
            quantity=1,
            unit_price=Decimal('25.00'),
            is_fulfilled=False
        )
        
        # Test with one unfulfilled item
        self.order.update_status()
        self.assertEqual(self.order.status, 'processing')
        self.assertFalse(self.order.is_fulfilled)
        
        # Mark all items as fulfilled
        order_item2.is_fulfilled = True
        order_item2.save()
        
        # Test with all items fulfilled
        self.order.update_status()
        self.assertEqual(self.order.status, 'fulfilled')
        self.assertTrue(self.order.is_fulfilled)


class OrderItemModelTests(TransactionTestCase):
    def setUp(self):
        test_name = self._testMethodName
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('100.00'),
            status='pending',
            is_fulfilled=False
        )
        
        # Create product, seller, inventory
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.seller = User.objects.create_user(
            email=f'seller_{test_name}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=False
        )

    def test_order_item_creation(self):
        """Test that an order item can be created with the correct fields"""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.inventory, self.inventory)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.unit_price, Decimal('25.00'))
        self.assertFalse(self.order_item.is_fulfilled)
        self.assertIsNone(self.order_item.fulfilled_at)
        self.assertIsNotNone(self.order_item.created_at)

    def test_order_item_string_representation(self):
        """Test the string representation of an order item"""
        self.assertEqual(str(self.order_item), "2 x Test Product")

    def test_subtotal(self):
        """Test subtotal property"""
        self.assertEqual(self.order_item.subtotal, Decimal('50.00'))  # 2 * 25.00

    def test_mark_fulfilled(self):
        """Test mark_fulfilled method"""
        self.assertFalse(self.order_item.is_fulfilled)
        self.assertIsNone(self.order_item.fulfilled_at)
        
        self.order_item.mark_fulfilled()
        
        self.assertTrue(self.order_item.is_fulfilled)
        self.assertIsNotNone(self.order_item.fulfilled_at)
        
        # Check order status update
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'fulfilled')
        self.assertTrue(self.order.is_fulfilled)


class CartFormTests(TransactionTestCase):
    def setUp(self):
        test_name = self._testMethodName
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        self.cart = Cart.objects.create(user=self.user)
        
        # Create product, seller, inventory
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.seller = User.objects.create_user(
            email=f'seller_{test_name}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=self.inventory,
            quantity=2
        )

    def test_cart_item_form_valid_data(self):
        """Test cart item form with valid data"""
        form = CartItemForm({
            'quantity': 5
        }, instance=self.cart_item)
        self.assertTrue(form.is_valid())

    def test_cart_item_form_negative_quantity(self):
        """Test cart item form with negative quantity"""
        form = CartItemForm({
            'quantity': -1
        }, instance=self.cart_item)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_cart_item_form_quantity_exceeds_inventory(self):
        """Test cart item form with quantity exceeding inventory"""
        form = CartItemForm({
            'quantity': 20  # Inventory has only 10
        }, instance=self.cart_item)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_add_to_cart_form_valid_data(self):
        """Test add to cart form with valid data"""
        form = AddToCartForm({
            'inventory_id': self.inventory.id,
            'quantity': 3
        })
        self.assertTrue(form.is_valid())

    def test_add_to_cart_form_negative_quantity(self):
        """Test add to cart form with negative quantity"""
        form = AddToCartForm({
            'inventory_id': self.inventory.id,
            'quantity': -1
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_checkout_form_valid_data(self):
        """Test checkout form with valid data"""
        # Add balance to user
        self.user.add_to_balance('100.00')
        
        form = CheckoutForm({
            'confirm': True
        }, user=self.user, cart=self.cart)
        self.assertTrue(form.is_valid())

    def test_checkout_form_insufficient_balance(self):
        """Test checkout form with insufficient balance"""
        form = CheckoutForm({
            'confirm': True
        }, user=self.user, cart=self.cart)
        self.assertFalse(form.is_valid())
        # Should have a non-field error
        self.assertTrue(form.non_field_errors())


class CartViewsTests(TransactionTestCase):
    def setUp(self):
        test_name = self._testMethodName
        self.client = Client()
        self.user = User.objects.create_user(
            email=f'testuser_{test_name}@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        self.client.login(email=self.user.email, password='testpassword123')
        
        # Delete any existing carts for this user to avoid OneToOne constraint violations
        Cart.objects.filter(user=self.user).delete()
        
        # Create cart
        self.cart = Cart.objects.create(user=self.user)
        
        # Create product, seller, inventory
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.seller = User.objects.create_user(
            email=f'seller_{test_name}@example.com',
            password='password123',
            full_name='Test Seller',
            address='Seller St'
        )
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Add item to cart
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=self.inventory,
            quantity=2
        )

    def test_cart_view(self):
        """Test cart view"""
        response = self.client.get(reverse('carts:view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/cart.html')
        self.assertContains(response, 'Test Product')

    def test_add_to_cart(self):
        """Test add to cart view"""
        # Clear cart first
        self.cart.clear()
        
        response = self.client.post(reverse('carts:add'), {
            'inventory_id': self.inventory.id,
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if item was added
        self.assertEqual(self.cart.items.count(), 1)
        cart_item = self.cart.items.first()
        self.assertEqual(cart_item.quantity, 3)

    def test_update_cart_item(self):
        """Test update cart item view"""
        response = self.client.post(reverse('carts:update_item', kwargs={'item_id': self.cart_item.id}), {
            'quantity': 5
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if item was updated
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)

    def test_remove_from_cart(self):
        """Test remove from cart view"""
        response = self.client.post(reverse('carts:remove_item', kwargs={'item_id': self.cart_item.id}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if item was removed
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout(self):
        """Test checkout view"""
        # Add balance to user
        self.user.add_to_balance('100.00')
        
        response = self.client.get(reverse('carts:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/checkout.html')
        
        # Test successful checkout
        response = self.client.post(reverse('carts:checkout'), {
            'confirm': True
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to order detail
        
        # Check if order was created
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, Decimal('50.00'))  # 2 * 25.00
        
        # Check if cart was cleared
        self.assertEqual(self.cart.items.count(), 0)
        
        # Check if user balance was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('50.00'))  # 100.00 - 50.00
        
        # Check if inventory was updated
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 8)  # 10 - 2
        
        # Check if seller balance was updated
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.balance, Decimal('50.00'))  # 0 + 50.00

    def test_order_list_view(self):
        """Test order list view"""
        # Create an order
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('50.00'),
            status='pending',
            is_fulfilled=False
        )
        
        response = self.client.get(reverse('carts:orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/order_list.html')
        self.assertContains(response, f'Order #{order.id}')

    def test_order_detail_view(self):
        """Test order detail view"""
        # Create an order
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('50.00'),
            status='pending',
            is_fulfilled=False
        )
        
        # Add order item
        order_item = OrderItem.objects.create(
            order=order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=False
        )
        
        response = self.client.get(reverse('carts:order_detail', kwargs={'pk': order.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/order_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '50.00')  # Total amount

    def test_cancel_order(self):
        """Test cancel order view"""
        # Create an order
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('50.00'),
            status='pending',
            is_fulfilled=False
        )
        
        # Add order item
        order_item = OrderItem.objects.create(
            order=order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=False
        )
        
        # Update inventory to simulate purchase
        self.inventory.quantity = 8  # Original 10 - 2
        self.inventory.save()
        
        # Add balance to seller to simulate payment
        self.seller.add_to_balance('50.00')
        
        response = self.client.post(reverse('carts:cancel_order', kwargs={'pk': order.id}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if order was canceled
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')
        
        # Check if inventory was restored
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 10)  # 8 + 2
        
        # Check if user balance was refunded
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('50.00'))  # 0 + 50.00
        
        # Check if seller balance was deducted
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.balance, Decimal('0.00'))  # 50.00 - 50.00
