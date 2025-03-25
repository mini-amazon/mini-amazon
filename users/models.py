from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserManager(BaseUserManager):
    """
    Custom user manager for User model with email as the unique identifier.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with email as the unique identifier instead of username.
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)
    address = models.TextField(_('address'))
    balance = models.DecimalField(
        _('balance'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'address']

    objects = UserManager()

    def __str__(self):
        return self.email

    def add_to_balance(self, amount):
        """
        Add to the user's balance.
        """
        self.balance += Decimal(amount)
        self.save()
        return True

    def withdraw_from_balance(self, amount):
        """
        Withdraw from the user's balance if sufficient funds exist.
        """
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False
