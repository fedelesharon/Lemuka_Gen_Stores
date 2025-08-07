from django.contrib import admin
from .models import Product, Stock

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = ('name', 'quantity', 'price')  # ✅ Remove 'category' unless you’ve added that field  # Use actual Product model fields
   search_fields = ['name', 'cereal_type']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_kg', 'date_added']
    list_filter = ['date_added']

