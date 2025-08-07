from django.urls import path
from . import views
from .views import record_sale

urlpatterns = [
    path('', views.product_list, name='product_list'),
      path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('sale/', views.record_sale, name='record_sale'),
     path('chart-data/sales/', views.sales_chart_data, name='sales_chart_data'),
    path('chart-data/stock/', views.stock_chart_data, name='stock_chart_data'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('reports/sales/pdf/', views.sales_report_pdf, name='sales_report_pdf'),

]
