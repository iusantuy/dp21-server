# invoices/urls.py
from django.urls import path
from .presentation.views import InvoiceCreateView, InvoiceDetailView, InvoicePreviewView, SuratJalanPreviewView

urlpatterns = [
    # path("", InvoiceCreateView.as_view(), name="create-invoice"),
    path("<int:id>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("invoice/", InvoicePreviewView.as_view(), name="invoice-preview"),
    path("surat-jalan/", SuratJalanPreviewView.as_view(), name="surat-jalan-preview"),
    path("create/", InvoiceCreateView.as_view(), name="invoice-create"),
]
