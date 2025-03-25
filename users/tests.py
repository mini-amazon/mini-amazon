from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .forms import UserRegistrationForm, UserUpdateForm, PasswordChangeForm, BalanceUpdateForm

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )

    def test_user_creation(self):
        """Test that a user can be created with the correct fields"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.address, '123 Test St')
        self.assertEqual(self.user.balance, Decimal('0.00'))
        self.assertTrue(self.user.check_password('testpassword123'))

    def test_user_string_representation(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_add_to_balance(self):
        """Test that balance can be added correctly"""
        self.user.add_to_balance('50.00')
        self.assertEqual(self.user.balance, Decimal('50.00'))
        
        self.user.add_to_balance('25.50')
        self.assertEqual(self.user.balance, Decimal('75.50'))

    def test_withdraw_from_balance(self):
        """Test that balance can be withdrawn correctly"""
        self.user.add_to_balance('100.00')
        self.assertEqual(self.user.balance, Decimal('100.00'))
        
        # Valid withdrawal
        result = self.user.withdraw_from_balance('50.00')
        self.assertTrue(result)
        self.assertEqual(self.user.balance, Decimal('50.00'))
        
        # Invalid withdrawal (insufficient funds)
        result = self.user.withdraw_from_balance('100.00')
        self.assertFalse(result)
        self.assertEqual(self.user.balance, Decimal('50.00'))  # Balance unchanged


class UserFormTests(TestCase):
    def test_user_registration_form_valid_data(self):
        """Test registration form with valid data"""
        form = UserRegistrationForm({
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'address': '456 New St',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        })
        self.assertTrue(form.is_valid())

    def test_user_registration_form_password_mismatch(self):
        """Test registration form with mismatched passwords"""
        form = UserRegistrationForm({
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'address': '456 New St',
            'password1': 'securepassword123',
            'password2': 'differentpassword123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_update_form_valid_data(self):
        """Test user update form with valid data"""
        form = UserUpdateForm({
            'full_name': 'Updated Name',
            'address': 'Updated Address',
        })
        self.assertTrue(form.is_valid())

    def test_balance_update_form_valid_data(self):
        """Test balance update form with valid data"""
        form = BalanceUpdateForm({
            'amount': '50.00',
            'action': 'add',
        })
        self.assertTrue(form.is_valid())

    def test_balance_update_form_negative_amount(self):
        """Test balance update form with negative amount"""
        form = BalanceUpdateForm({
            'amount': '-10.00',
            'action': 'add',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            full_name='Test User',
            address='123 Test St'
        )
        self.client.login(email='testuser@example.com', password='testpassword123')

    def test_user_registration_view(self):
        """Test user registration view"""
        # Logout first since we're logged in from setUp
        self.client.logout()
        
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        # Test registration with valid data
        response = self.client.post(reverse('users:register'), {
            'email': 'newuser2@example.com',
            'full_name': 'New User',
            'address': '789 New St',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(email='newuser2@example.com').exists())

    def test_user_profile_view(self):
        """Test user profile view"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_balance_view(self):
        """Test balance view"""
        response = self.client.get(reverse('users:balance'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/balance.html')

        # Test adding balance
        response = self.client.post(reverse('users:balance'), {
            'amount': '100.00',
            'action': 'add',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('100.00'))

    def test_purchase_history_view(self):
        """Test purchase history view"""
        response = self.client.get(reverse('users:purchase_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/purchase_history.html')

    def test_public_profile_view(self):
        """Test public profile view"""
        response = self.client.get(reverse('users:public_profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/public_profile.html')
        
    def test_login_required(self):
        """Test that views require login"""
        self.client.logout()
        
        response = self.client.get(reverse('users:profile'))
        self.assertNotEqual(response.status_code, 200)  # Should not be accessible when logged out
