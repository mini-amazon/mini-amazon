from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

from .models import ProductReview, SellerReview, Message
from .forms import ProductReviewForm, SellerReviewForm, MessageForm
from products.models import Product, Category
from carts.models import Order, OrderItem
from sellers.models import Inventory

User = get_user_model()


class ProductReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
            created_by=self.user
        )
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='This is a great product!'
        )

    def test_product_review_creation(self):
        """Test that a product review can be created with the correct fields"""
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'This is a great product!')
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNotNone(self.review.updated_at)

    def test_product_review_string_representation(self):
        """Test the string representation of a product review"""
        self.assertEqual(str(self.review), f"Review by {self.user.email} for {self.product.name}")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.review.get_absolute_url(),
            reverse('products:detail', kwargs={'pk': self.product.pk})
        )


class SellerReviewModelTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            email='buyer@example.com',
            password='testpassword123',
            full_name='Test Buyer',
            address='123 Buyer St'
        )
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
        
        # Create an order
        self.order = Order.objects.create(
            user=self.buyer,
            total_amount=Decimal('50.00'),
            status='fulfilled',
            is_fulfilled=True
        )
        
        # Create inventory
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Create order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=True
        )
        
        # Create seller review
        self.review = SellerReview.objects.create(
            seller=self.seller,
            user=self.buyer,
            order=self.order,
            rating=5,
            comment='Great seller, fast shipping!'
        )

    def test_seller_review_creation(self):
        """Test that a seller review can be created with the correct fields"""
        self.assertEqual(self.review.seller, self.seller)
        self.assertEqual(self.review.user, self.buyer)
        self.assertEqual(self.review.order, self.order)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great seller, fast shipping!')
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNotNone(self.review.updated_at)

    def test_seller_review_string_representation(self):
        """Test the string representation of a seller review"""
        self.assertEqual(str(self.review), f"Review by {self.buyer.email} for {self.seller.email}")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.review.get_absolute_url(),
            reverse('users:public_profile', kwargs={'pk': self.seller.pk})
        )


class MessageModelTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            email='buyer@example.com',
            password='testpassword123',
            full_name='Test Buyer',
            address='123 Buyer St'
        )
        self.seller = User.objects.create_user(
            email='seller@example.com',
            password='testpassword123',
            full_name='Test Seller',
            address='123 Seller St'
        )
        
        # Create an order
        self.order = Order.objects.create(
            user=self.buyer,
            total_amount=Decimal('50.00'),
            status='fulfilled',
            is_fulfilled=True
        )
        
        # Create message
        self.message = Message.objects.create(
            sender=self.buyer,
            receiver=self.seller,
            order=self.order,
            content='When will my order be shipped?',
            is_read=False
        )

    def test_message_creation(self):
        """Test that a message can be created with the correct fields"""
        self.assertEqual(self.message.sender, self.buyer)
        self.assertEqual(self.message.receiver, self.seller)
        self.assertEqual(self.message.order, self.order)
        self.assertEqual(self.message.content, 'When will my order be shipped?')
        self.assertFalse(self.message.is_read)
        self.assertIsNotNone(self.message.created_at)

    def test_message_string_representation(self):
        """Test the string representation of a message"""
        self.assertEqual(str(self.message), f"Message from {self.buyer.email} to {self.seller.email}")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.message.get_absolute_url(),
            reverse('social:conversation', kwargs={'user_id': self.seller.id})
        )


class SocialFormTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            email='buyer@example.com',
            password='testpassword123',
            full_name='Test Buyer',
            address='123 Buyer St'
        )
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
        
        # Create an order
        self.order = Order.objects.create(
            user=self.buyer,
            total_amount=Decimal('50.00'),
            status='fulfilled',
            is_fulfilled=True
        )
        
        # Create inventory
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Create order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=True
        )

    def test_product_review_form_valid_data(self):
        """Test product review form with valid data"""
        form = ProductReviewForm({
            'rating': 4,
            'comment': 'This is a great product!'
        }, user=self.buyer, product=self.product)
        self.assertTrue(form.is_valid())

    def test_product_review_form_rating_out_of_range(self):
        """Test product review form with rating out of range"""
        form = ProductReviewForm({
            'rating': 6,  # Rating should be 1-5
            'comment': 'This is a great product!'
        }, user=self.buyer, product=self.product)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_seller_review_form_valid_data(self):
        """Test seller review form with valid data"""
        form = SellerReviewForm({
            'order': self.order.id,
            'rating': 5,
            'comment': 'Great seller, fast shipping!'
        }, user=self.buyer, seller=self.seller)
        self.assertTrue(form.is_valid())

    def test_seller_review_form_no_order(self):
        """Test seller review form with no order selected"""
        form = SellerReviewForm({
            'rating': 5,
            'comment': 'Great seller, fast shipping!'
        }, user=self.buyer, seller=self.seller)
        self.assertFalse(form.is_valid())
        self.assertIn('order', form.errors)

    def test_message_form_valid_data(self):
        """Test message form with valid data"""
        form = MessageForm({
            'content': 'When will my order be shipped?'
        }, sender=self.buyer, receiver=self.seller)
        self.assertTrue(form.is_valid())

    def test_message_form_empty_content(self):
        """Test message form with empty content"""
        form = MessageForm({
            'content': ''
        }, sender=self.buyer, receiver=self.seller)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


class SocialViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            email='buyer@example.com',
            password='testpassword123',
            full_name='Test Buyer',
            address='123 Buyer St'
        )
        self.client.login(email='buyer@example.com', password='testpassword123')
        
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
        
        # Create an order
        self.order = Order.objects.create(
            user=self.buyer,
            total_amount=Decimal('50.00'),
            status='fulfilled',
            is_fulfilled=True
        )
        
        # Create inventory
        self.inventory = Inventory.objects.create(
            seller=self.seller,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        
        # Create order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            inventory=self.inventory,
            quantity=2,
            unit_price=Decimal('25.00'),
            is_fulfilled=True
        )
        
        # Create reviews
        self.product_review = ProductReview.objects.create(
            product=self.product,
            user=self.buyer,
            rating=4,
            comment='This is a great product!'
        )
        
        self.seller_review = SellerReview.objects.create(
            seller=self.seller,
            user=self.buyer,
            order=self.order,
            rating=5,
            comment='Great seller, fast shipping!'
        )
        
        # Create messages
        self.message_from_buyer = Message.objects.create(
            sender=self.buyer,
            receiver=self.seller,
            order=self.order,
            content='When will my order be shipped?',
            is_read=False
        )
        
        self.message_from_seller = Message.objects.create(
            sender=self.seller,
            receiver=self.buyer,
            order=self.order,
            content='Your order has been shipped!',
            is_read=False
        )

    def test_create_product_review_view(self):
        """Test create product review view"""
        # Delete existing review to test creation
        self.product_review.delete()
        
        response = self.client.get(reverse('social:product_review', kwargs={'product_id': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/product_review_form.html')
        
        # Test creating a review
        response = self.client.post(reverse('social:product_review', kwargs={'product_id': self.product.pk}), {
            'rating': 4,
            'comment': 'This is a new review!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was created
        self.assertTrue(ProductReview.objects.filter(product=self.product, user=self.buyer).exists())
        new_review = ProductReview.objects.get(product=self.product, user=self.buyer)
        self.assertEqual(new_review.rating, 4)
        self.assertEqual(new_review.comment, 'This is a new review!')

    def test_update_product_review_view(self):
        """Test update product review view"""
        response = self.client.get(reverse('social:product_review', kwargs={'product_id': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/product_review_form.html')
        
        # Test updating a review
        response = self.client.post(reverse('social:product_review', kwargs={'product_id': self.product.pk}), {
            'rating': 5,
            'comment': 'This is an updated review!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was updated
        self.product_review.refresh_from_db()
        self.assertEqual(self.product_review.rating, 5)
        self.assertEqual(self.product_review.comment, 'This is an updated review!')

    def test_delete_product_review_view(self):
        """Test delete product review view"""
        response = self.client.get(reverse('social:delete_product_review', kwargs={'review_id': self.product_review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/product_review_confirm_delete.html')
        
        # Test deleting a review
        response = self.client.post(reverse('social:delete_product_review', kwargs={'review_id': self.product_review.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was deleted
        self.assertFalse(ProductReview.objects.filter(pk=self.product_review.pk).exists())

    def test_create_seller_review_view(self):
        """Test create seller review view"""
        # Delete existing review to test creation
        self.seller_review.delete()
        
        response = self.client.get(reverse('social:seller_review', kwargs={'seller_id': self.seller.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/seller_review_form.html')
        
        # Test creating a review
        response = self.client.post(reverse('social:seller_review', kwargs={'seller_id': self.seller.pk}), {
            'order': self.order.id,
            'rating': 5,
            'comment': 'This is a new seller review!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was created
        self.assertTrue(SellerReview.objects.filter(seller=self.seller, user=self.buyer).exists())
        new_review = SellerReview.objects.get(seller=self.seller, user=self.buyer)
        self.assertEqual(new_review.rating, 5)
        self.assertEqual(new_review.comment, 'This is a new seller review!')

    def test_update_seller_review_view(self):
        """Test update seller review view"""
        response = self.client.get(reverse('social:seller_review', kwargs={'seller_id': self.seller.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/seller_review_form.html')
        
        # Test updating a review
        response = self.client.post(reverse('social:seller_review', kwargs={'seller_id': self.seller.pk}), {
            'order': self.order.id,
            'rating': 4,
            'comment': 'This is an updated seller review!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was updated
        self.seller_review.refresh_from_db()
        self.assertEqual(self.seller_review.rating, 4)
        self.assertEqual(self.seller_review.comment, 'This is an updated seller review!')

    def test_delete_seller_review_view(self):
        """Test delete seller review view"""
        response = self.client.get(reverse('social:delete_seller_review', kwargs={'review_id': self.seller_review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/seller_review_confirm_delete.html')
        
        # Test deleting a review
        response = self.client.post(reverse('social:delete_seller_review', kwargs={'review_id': self.seller_review.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if review was deleted
        self.assertFalse(SellerReview.objects.filter(pk=self.seller_review.pk).exists())

    def test_user_reviews_list_view(self):
        """Test user reviews list view"""
        response = self.client.get(reverse('social:my_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/user_reviews.html')
        self.assertContains(response, 'This is a great product!')
        self.assertContains(response, 'Great seller, fast shipping!')

    def test_conversation_list_view(self):
        """Test conversation list view"""
        response = self.client.get(reverse('social:conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/conversation_list.html')
        self.assertContains(response, 'Test Seller')

    def test_conversation_detail_view(self):
        """Test conversation detail view"""
        response = self.client.get(reverse('social:conversation', kwargs={'user_id': self.seller.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/conversation_detail.html')
        self.assertContains(response, 'When will my order be shipped?')
        self.assertContains(response, 'Your order has been shipped!')
        
        # Test sending a message
        response = self.client.post(reverse('social:conversation', kwargs={'user_id': self.seller.pk}), {
            'content': 'Thank you for the update!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Check if message was sent
        newest_message = Message.objects.filter(sender=self.buyer, receiver=self.seller).order_by('-created_at').first()
        self.assertEqual(newest_message.content, 'Thank you for the update!')

    def test_marking_messages_as_read(self):
        """Test that messages are marked as read when viewing a conversation"""
        # Initially, the message from seller is unread
        self.assertFalse(self.message_from_seller.is_read)
        
        # View the conversation
        self.client.get(reverse('social:conversation', kwargs={'user_id': self.seller.pk}))
        
        # Check if message was marked as read
        self.message_from_seller.refresh_from_db()
        self.assertTrue(self.message_from_seller.is_read)
