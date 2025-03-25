from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

from .models import Product, Category
from .forms import ProductForm, ProductSearchForm
from sellers.models import Inventory

User = get_user_model()


class CategoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )

    def test_category_creation(self):
        """Test that a category can be created with the correct fields"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Electronic devices and gadgets')
        self.assertIsNotNone(self.category.created_at)

    def test_category_string_representation(self):
        """Test the string representation of a category"""
        self.assertEqual(str(self.category), 'Electronics')

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse('products:category', kwargs={'category_id': self.category.pk})
        )


class ProductModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            category=self.category,
            created_by=self.user
        )

    def test_product_creation(self):
        """Test that a product can be created with the correct fields"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'This is a test product')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.created_by, self.user)
        self.assertIsNotNone(self.product.created_at)
        self.assertIsNotNone(self.product.updated_at)

    def test_product_string_representation(self):
        """Test the string representation of a product"""
        self.assertEqual(str(self.product), 'Test Product')

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse('products:detail', kwargs={'pk': self.product.pk})
        )

    def test_min_price_no_inventory(self):
        """Test min_price property with no inventory"""
        self.assertEqual(self.product.min_price, Decimal('0.00'))

    def test_min_price_with_inventory(self):
        """Test min_price property with inventory"""
        seller1 = User.objects.create_user(
            email='seller1@example.com',
            password='password123',
            full_name='Seller One',
            address='Seller St'
        )
        seller2 = User.objects.create_user(
            email='seller2@example.com',
            password='password123',
            full_name='Seller Two',
            address='Seller Ave'
        )
        
        # Create inventories
        inventory1 = Inventory.objects.create(
            seller=seller1,
            product=self.product,
            quantity=10,
            price=Decimal('25.00')
        )
        inventory2 = Inventory.objects.create(
            seller=seller2,
            product=self.product,
            quantity=5,
            price=Decimal('20.00')
        )
        
        self.assertEqual(self.product.min_price, Decimal('20.00'))


class ProductFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.image = SimpleUploadedFile(
            'test.gif', self.small_gif, content_type='image/gif'
        )

    def test_product_form_valid_data_no_image(self):
        """Test product form with valid data but no image"""
        form = ProductForm({
            'name': 'New Product',
            'description': 'A new product description',
            'category': self.category.pk,
        })
        self.assertTrue(form.is_valid())

    def test_product_form_valid_data_with_image(self):
        """Test product form with valid data and an image"""
        form = ProductForm({
            'name': 'New Product',
            'description': 'A new product description',
            'category': self.category.pk,
        }, {'image': self.image})
        self.assertTrue(form.is_valid())

    def test_product_form_missing_required_fields(self):
        """Test product form with missing required fields"""
        form = ProductForm({
            'name': '',  # Missing name
            'description': 'A product description',
            'category': self.category.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_product_search_form(self):
        """Test product search form"""
        form = ProductSearchForm({
            'query': 'test',
            'category': self.category.pk,
            'min_price': '10.00',
            'max_price': '50.00',
            'sort_by': 'price_asc',
        })
        self.assertTrue(form.is_valid())


class ProductViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            category=self.category,
            created_by=self.user
        )
        
        # Create a seller and inventory
        self.seller = User.objects.create_user(
            email='seller@example.com',
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

    def test_product_list_view(self):
        """Test product list view"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(reverse('products:detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'This is a test product')

    def test_product_search_view(self):
        """Test product search view"""
        response = self.client.get(reverse('products:search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_search.html')
        self.assertContains(response, 'Test Product')

    def test_product_create_view(self):
        """Test product create view"""
        response = self.client.get(reverse('products:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_create.html')
        
        # Test creating a product
        response = self.client.post(reverse('products:create'), {
            'name': 'New Test Product',
            'description': 'A new test product description',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertTrue(Product.objects.filter(name='New Test Product').exists())

    def test_product_update_view(self):
        """Test product update view"""
        response = self.client.get(reverse('products:update', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_update.html')
        
        # Test updating a product
        response = self.client.post(reverse('products:update', kwargs={'pk': self.product.pk}), {
            'name': 'Updated Product Name',
            'description': 'Updated product description',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        
        # Refresh from database
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product Name')
        self.assertEqual(self.product.description, 'Updated product description')

    def test_category_view(self):
        """Test category view"""
        response = self.client.get(reverse('products:category', kwargs={'category_id': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Product')

    def test_category_list_view(self):
        """Test category list view"""
        response = self.client.get(reverse('products:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_list.html')
        self.assertContains(response, 'Electronics')
