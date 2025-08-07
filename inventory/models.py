from django.db import models
from django.utils import timezone

class Product(models.Model):
    CEREAL_TYPES = [
        ('maize', 'Maize'),
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
        ('millet', 'Millet'),
        ('sorghum', 'Sorghum'),
        ('oats', 'Oats'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CEREAL_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_entries')
    quantity_kg = models.PositiveIntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_kg}kg"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    date_sold = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity_sold} of {self.product.name} on {self.date_sold.strftime('%Y-%m-%d')}"
