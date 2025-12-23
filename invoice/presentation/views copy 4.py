# invoices/presentation/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import render
from django.views import View
import json
from decimal import Decimal

from ..infrastructure.models import Invoice
from ..presentation.serializers import (
    InvoiceSerializer,
    InvoiceResponseSerializer,
)

from ..application.services.invoice_service import InvoiceService
from ..utils.invoice_utils import generate_invoice_number


class InvoiceCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        """
        DRF method to create object — logic utama dipindah ke InvoiceService.
        """
        validated_data = serializer.validated_data

        # Tambahkan invoice_number hasil util
        customer = validated_data.get("to")
        validated_data["invoice_number"] = generate_invoice_number(customer)

        # Kirim ke service → create invoice + items + hitung total
        invoice_entity = InvoiceService.create_invoice(validated_data)

        # Simpan untuk response
        self.invoice_entity = invoice_entity

    def create(self, request, *args, **kwargs):
        """
        Custom response agar pakai InvoiceResponseSerializer.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform_create dipanggil otomatis oleh DRF
        self.perform_create(serializer)

        response_serializer = InvoiceResponseSerializer(self.invoice_entity)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.prefetch_related("items").all()
    serializer_class = InvoiceResponseSerializer
    lookup_field = "id"


class InvoicePreviewView(View):
    """
    Generate preview invoice (HTML) sebelum disimpan.
    """

    def post(self, request):
        data = json.loads(request.body)

        # ========== Generate Invoice Number ==========
        to = data.get("to", "").strip().title()
        dp = Decimal(data.get("dp", 0))
        invoice_number = generate_invoice_number(to)

        # ========== Hitung total item ==========
        items = data.get("items", [])
        subtotal = sum(int(i.get("quantity", 0)) * Decimal(i.get("price", 0)) for i in items)
        total = subtotal - dp
        # ========== Watermark ==========
        watermarks = [{"top": f"{y}%", "left": f"{x}%"} 
                      for y in range(0, 100, 25) 
                      for x in range(0, 100, 25)]

        # ========== Data untuk template ==========
        invoice = {
            "store_name": "Dolce Papa 21",
            "store_logo_url": request.build_absolute_uri('/media/logo/dp21-logo.jpg'),
            "invoice_number": invoice_number,
            "date": data.get("due_date", ""),
            "customer_name": to,
            "contact": "Jln. Villa Bandung Indah No.14, Cileunyi - Bandung",
            "payment_method": "Bank BCA (Fakhri Abdullah Azzam) 6640 4166 78",
            "ket": "Mohon lakukan pembayaran satu hari setelah produk diterima.",
            "items": items,
            "dp": dp,
            "subtotal": subtotal,
            "total": total,
            "notes": data.get("notes", ""),
            "watermarks": watermarks
        }
        # print(items)
        # print(total)

        return render(request, "invoice_template.html", invoice)
