from django.urls import path
from . import views

urlpatterns = [
    path('temperature/', views.temperature_plot, name='temperature_plot'),
    path('sales/', views.sales_analysis, name='sales_analysis'),
]