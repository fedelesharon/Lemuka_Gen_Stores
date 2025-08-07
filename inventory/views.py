from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from .forms import SaleForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Sale
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .models import Sale
from .models import Stock
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Sale, Product


def product_list(request):
    """Display all products in the system."""
    products = Product.objects.all().order_by('-created_at')  # if you have a created_at field
    return render(request, 'inventory/product_list.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()
            # Deduct sold quantity from product stock
            sale.product.stock -= sale.quantity_sold
            sale.product.save()
            return redirect('sales_list')
    else:
        form = SaleForm()
    return render(request, 'record_sale.html', {'form': form})

def sales_chart_data(request):
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    labels = [day.strftime('%Y-%m-%d') for day in last_7_days]
    data = []

    for day in last_7_days:
        total = Sale.objects.filter(sale_date=day).aggregate(Sum('total_price'))['total_price__sum'] or 0
        data.append(total)

    return JsonResponse({'labels': labels, 'data': data})

def dashboard(request):
    context = {
        'total_products': 140,
        'items_in_stock': 110,
        'low_stock': 20,
        'out_of_stock': 10,
        'products': [
            {'name': 'Maize Flour', 'quantity': 25, 'price': 120, 'last_updated': '2025-08-05', 'category': 'Flour'},
            {'name': 'Wheat Flour', 'quantity': 10, 'price': 135, 'last_updated': '2025-08-06', 'category': 'Flour'},
            {'name': 'Rice', 'quantity': 30, 'price': 160, 'last_updated': '2025-08-06', 'category': 'Cereals'},
            {'name': 'Green Grams', 'quantity': 15, 'price': 180, 'last_updated': '2025-08-07', 'category': 'Cereals'},
            {'name': 'Beans', 'quantity': 20, 'price': 150, 'last_updated': '2025-08-07', 'category': 'Cereals'},
            # Add more cereal or non-cereal products as needed
        ]
    }
    return render(request, 'inventory/dashboard.html', context)



def stock_chart_data(request):
    stocks = Stock.objects.select_related('product').all()

    labels = [stock.product.name for stock in stocks]
    data = [stock.quantity for stock in stocks]

    return JsonResponse({
        'labels': labels,
        'data': data,
    })


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def sales_report_pdf(request):
    sales = Sale.objects.select_related('product').all()
    return render_to_pdf('reports/sales_report.html', {'sales': sales})