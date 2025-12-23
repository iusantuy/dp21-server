# invoices/presentation/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import render
from django.views import View
import json
from decimal import Decimal
from ..utils.decimal import safe_decimal

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
    def post(self, request):
        data = json.loads(request.body)

        # Nama customer
        # to = data.get("to", "").strip().title()
        to = data.get("to", "").strip()
        dp = Decimal(data.get("dp", 0))
        # dp = safe_decimal(data.get("dp", 0))

        # Generate invoice number sesuai customer
        invoice_number = generate_invoice_number(to)

        # Hitung total item
        items = data.get("items", [])
        subtotal = sum(
            int(i.get("quantity", 0)) * Decimal(i.get("price", 0))
            for i in items
        )
        total = subtotal - dp

        # font_size_px = 48
        # # estimasi panjang teks, misal 10 karakter * 24px per karakter
        # store_name = "Dolce Papa 21"
        # text_width_px = len(store_name) * 24  

        # # panjang diagonal span setelah rotate -45°
        # diagonal = math.sqrt(font_size_px**2 + text_width_px**2)  

        # # ubah ke % halaman (asumsi A4 = 210mm x 297mm)
        # page_width_px = 2100  # misal 10px per mm
        # page_height_px = 2970

        # spacing_x = diagonal / page_width_px * 100
        # spacing_y = diagonal / page_height_px * 100

        # watermarks = [
        #     {"top": f"{y}%", "left": f"{x}%"} 
        #     for y in range(0, 100, int(spacing_y)) 
        #     for x in range(0, 100, int(spacing_x))
        # ]

        # Watermark
        # watermarks = [{"top": f"{y}%", "left": f"{x}%"} 
        #               for y in range(0, 100, 20) 
        #               for x in range(0, 100, 20)]

        # estimasi spacing untuk watermark miring
        spacing_x = 25  # horizontal %
        spacing_y = 30  # vertical %

        watermarks = [
            {"top": f"{y}%", "left": f"{x}%"} 
            for y in range(0, 100, spacing_y) 
            for x in range(0, 100, spacing_x)
        ]

        invoice = {
            "store_name": "Dolce Papa 21",
            "store_logo_url": request.build_absolute_uri('/media/logo/logo dolce papa.jpg'),
            "invoice_number": invoice_number,
            "date": data.get("due_date", ""),
            "customer_name": to,
            "address": "Jln. Villa Bandung Indah No.14, Cileunyi - Bandung",
            "contact": "Fakhri Abdullah Azzam",
            "phone_number": "+62 878 9386 3007",
            "payment_method": "Bank Mandiri an. Fakhri Abdullah Azzam ",
            "ket": "Mohon lakukan pembayaran satu hari setelah produk diterima dan invoice ditanda tangani",
            "items": items,
            "dp": dp,
            "subtotal": subtotal,
            "total": total,
            "notes": data.get("notes", ""),
            "watermarks": watermarks
        }

        return render(request, "invoice_template.html", invoice)
    
class SuratJalanPreviewView(View):
    def post(self, request):
        data = json.loads(request.body)

        # Nama customer
        # to = data.get("to", "").strip().title()
        to = data.get("to", "").strip()
        # dp = Decimal(data.get("dp", 0))
        dp = safe_decimal(data.get("dp", 0))

        # Generate invoice number sesuai customer
        surat_jalan_number = generate_invoice_number(to)

        # Hitung total item
        items = data.get("items", [])
        subtotal = sum(
            int(i.get("quantity", 0)) * Decimal(i.get("price", 0))
            for i in items
        )
        total = subtotal - dp

        # Watermark
        watermarks = [{"top": f"{y}%", "left": f"{x}%"} 
                      for y in range(0, 100, 25) 
                      for x in range(0, 100, 25)]

        surat_jalan = {
            "store_name": "Dolce Papa 21",
            "store_logo_url": request.build_absolute_uri('/media/logo/logo dolce papa.jpg'),
            "surat_jalan_number": surat_jalan_number,
            "date": data.get("due_date", ""),
            "customer_name": to,
            "address": "Jln. Villa Bandung Indah No.14, Cileunyi - Bandung",
            "contact": "Fakhri Abdullah Azzam",
            "phone_number": "+62 878 9386 3007",
            "payment_method": "Bank Mandiri an. Fakhri Abdullah Azzam 13100 2456 0734",
            "ket": "Mohon lakukan pembayaran satu hari setelah produk diterima dan invoice ditanda tangani",
            "items": items,
            "dp": dp,
            "subtotal": subtotal,
            "total": total,
            "notes": data.get("notes", ""),
            "watermarks": watermarks
        }

        return render(request, "surat_jalan_template.html", surat_jalan)

