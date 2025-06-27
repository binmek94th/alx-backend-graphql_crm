import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()


from crm.models import Customer, Product, Order


def seed_customers():
    customers_data = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'phone': '+1234567890'},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'phone': '123-456-7890'},
        {'name': 'Carol White', 'email': 'carol@example.com', 'phone': None},
    ]
    customers = []
    for cdata in customers_data:
        customer, created = Customer.objects.get_or_create(email=cdata['email'], defaults=cdata)
        customers.append(customer)
    return customers

def seed_products():
    products_data = [
        {'name': 'Laptop', 'price': 999.99, 'stock': 10},
        {'name': 'Mouse', 'price': 25.50, 'stock': 100},
        {'name': 'Keyboard', 'price': 45.00, 'stock': 50},
    ]
    products = []
    for pdata in products_data:
        product, created = Product.objects.get_or_create(name=pdata['name'], defaults=pdata)
        products.append(product)
    return products

def seed_orders(customers, products):
    # Create a few orders with random customers and random products
    for i in range(5):
        customer = random.choice(customers)
        selected_products = random.sample(products, k=random.randint(1, len(products)))
        total_amount = sum(p.price for p in selected_products)
        order_date = timezone.now() - timedelta(days=random.randint(0, 30))

        order = Order.objects.create(customer=customer, total_amount=total_amount, order_date=order_date)
        order.products.set(selected_products)
        print(f"Created order {order.id} for {customer.name} with {len(selected_products)} products.")


def main():
    print("Seeding Customers...")
    customers = seed_customers()
    print(f"Seeded {len(customers)} customers.")

    print("Seeding Products...")
    products = seed_products()
    print(f"Seeded {len(products)} products.")

    print("Seeding Orders...")
    seed_orders(customers, products)
    print("Seeding completed.")

if __name__ == '__main__':
    main()
