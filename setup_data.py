import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniamazon.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Product, Category
from sellers.models import Inventory
from django.db.models import Q
from decimal import Decimal

User = get_user_model()

def setup_data():
    # 创建测试用户（一个买家，一个卖家）
    if not User.objects.filter(email='buyer@example.com').exists():
        buyer = User.objects.create_user(
            email='buyer@example.com',
            password='password123',
            full_name='Test Buyer',
            address='123 Buyer St',
            balance=1000.00
        )
        print("Created buyer user")
    else:
        buyer = User.objects.get(email='buyer@example.com')
        buyer.balance = 1000.00
        buyer.save()
        print("Updated buyer balance to $1000")
    
    if not User.objects.filter(email='seller@example.com').exists():
        seller = User.objects.create_user(
            email='seller@example.com',
            password='password123',
            full_name='Test Seller',
            address='123 Seller St',
            balance=0.00
        )
        print("Created seller user")
    else:
        seller = User.objects.get(email='seller@example.com')
    
    # 确保有分类
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)
    print("Ensured categories exist")
    
    # 创建一些测试产品
    electronics = Category.objects.get(name='Electronics')
    books = Category.objects.get(name='Books')
    
    # 创建电子产品
    if not Product.objects.filter(name='Smartphone X').exists():
        phone = Product.objects.create(
            name='Smartphone X',
            description='The latest smartphone with amazing features.',
            category=electronics,
            created_by=seller
        )
        print("Created Smartphone X product")
    else:
        phone = Product.objects.get(name='Smartphone X')
    
    if not Product.objects.filter(name='Laptop Pro').exists():
        laptop = Product.objects.create(
            name='Laptop Pro',
            description='Powerful laptop for professionals.',
            category=electronics,
            created_by=seller
        )
        print("Created Laptop Pro product")
    else:
        laptop = Product.objects.get(name='Laptop Pro')
    
    # 创建图书产品
    if not Product.objects.filter(name='Python Programming').exists():
        python_book = Product.objects.create(
            name='Python Programming',
            description='Learn Python programming from basics to advanced.',
            category=books,
            created_by=seller
        )
        print("Created Python Programming book")
    else:
        python_book = Product.objects.get(name='Python Programming')
    
    # 添加库存项目
    products = [phone, laptop, python_book]
    prices = [Decimal('699.99'), Decimal('1299.99'), Decimal('39.99')]
    quantities = [10, 5, 20]
    
    for product, price, quantity in zip(products, prices, quantities):
        inventory, created = Inventory.objects.get_or_create(
            seller=seller,
            product=product,
            defaults={
                'price': price,
                'quantity': quantity
            }
        )
        if not created:
            inventory.price = price
            inventory.quantity = quantity
            inventory.save()
            print(f"Updated inventory for {product.name}")
        else:
            print(f"Created inventory for {product.name}")
    
    print("Data setup complete!")

if __name__ == '__main__':
    setup_data() 