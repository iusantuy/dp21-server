# invoices/presentation/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils.crypto import get_random_string
from datetime import date
from decimal import Decimal

from invoice.infrastructure.models import Invoice, InvoiceItem
from invoice.presentation.serializers import InvoiceSerializer, InvoiceResponseSerializer


class InvoiceCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        """
        Handle invoice creation inside an atomic transaction.
        """
        # Generate unique invoice number
        today_str = date.today().strftime("%Y%m%d")
        random_str = get_random_string(3, allowed_chars="0123456789")
        invoice_number = f"INV-{today_str}-{random_str}"

        data = serializer.validated_data
        items_data = data.pop("items", [])

        # 1️⃣ Buat invoice kosong
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            **data,
            total=Decimal("0.00"),
        )

        # 2️⃣ Buat item + hitung total
        total = Decimal("0.00")
        for item in items_data:
            subtotal = Decimal(item["price"]) * item["quantity"]
            InvoiceItem.objects.create(
                invoice=invoice,
                name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )
            total += subtotal

        # 3️⃣ Update total invoice
        invoice.total = total
        invoice.save(update_fields=["total"])

        self.instance = invoice  # simpan instance untuk response

    def create(self, request, *args, **kwargs):
        """
        Override default create untuk return response custom.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = InvoiceResponseSerializer(self.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.prefetch_related("items").all()
    serializer_class = InvoiceResponseSerializer
    lookup_field = "id"



from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import render

class InvoicePreviewView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        store_name = data.get("store_name", "Toko Saya")
        store_address = data.get("store_address", "")
        customer_name = data.get("customer_name", "")
        customer_address = data.get("customer_address", "")
        items = data.get("items", [])
        notes = data.get("notes", "")
        total = data.get("total", 0)

        # Generate watermark positions (grid)
        watermarks = []
        for i in range(20):
            top = f"{(i % 5) * 20}%"
            left = f"{(i % 4) * 25}%"
            watermarks.append({"top": top, "left": left})

        return render(request, "invoice_template.html", {
            "store_name": store_name,
            "store_address": store_address,
            "customer_name": customer_name,
            "customer_address": customer_address,
            "items": items,
            "notes": notes,
            "total": total,
            "watermarks": watermarks,
        })



# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

# class InvoicePreviewView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         store_name = data.get("store_name", "My Store")
#         store_address = data.get("store_address", "")
#         customer_name = data.get("customer_name", "")
#         customer_address = data.get("customer_address", "")
#         items = data.get("items", [])
#         total = data.get("total", 0)
#         notes = data.get("notes", "")

#         # Hitung posisi watermark
#         watermarks = []
#         for i in range(20):
#             top = (i % 5) * 20
#             left = (i % 4) * 25
#             watermarks.append({"top": f"{top}%", "left": f"{left}%"})

#         return render(request, "invoice_template.html", {
#             "store_name": store_name,
#             "store_address": store_address,
#             "customer_name": customer_name,
#             "customer_address": customer_address,
#             "items": items,
#             "total": total,
#             "notes": notes,
#             "watermarks": watermarks,
#         })



# from django.http import HttpResponse
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny

# class InvoicePreviewView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         customer_name = data.get("customer_name")
#         items = data.get("items", [])
#         total = data.get("total")

#         # Render HTML preview (pakai CSS inline biar tampil rapih)
#         html = f"""
#         <html>
#         <head>
#           <title>Invoice Preview</title>
#           <style>
#             body {{ font-family: Arial; padding: 20px; }}
#             table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
#             th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
#             th {{ background-color: #f2f2f2; }}
#           </style>
#         </head>
#         <body>
#           <h2>Invoice Preview</h2>
#           <p><strong>Customer:</strong> {customer_name}</p>
#           <table>
#             <thead>
#               <tr><th>Item</th><th>Qty</th><th>Price</th></tr>
#             </thead>
#             <tbody>
#               {''.join([f"<tr><td>{i['name']}</td><td>{i['qty']}</td><td>{i['price']}</td></tr>" for i in items])}
#             </tbody>
#           </table>
#           <p style="margin-top:20px;"><strong>Total:</strong> ${total}</p>
#         </body>
#         </html>
#         """
#         return HttpResponse(html, content_type="text/html")










# from django.shortcuts import render

# # Create your views here.
# # invoices/views.py
# from rest_framework import generics
# from ..infrastructure.models import Invoice
# from ..serializers import InvoiceSerializer
# from django.utils.crypto import get_random_string
# from datetime import date

# class InvoiceCreateView(generics.CreateAPIView):
#     serializer_class = InvoiceSerializer

#     def perform_create(self, serializer):
#         # Generate invoice_number otomatis
#         today_str = date.today().strftime("%Y%m%d")
#         random_str = get_random_string(3, allowed_chars="0123456789")
#         invoice_number = f"INV-{today_str}-{random_str}"

#         items = self.request.data.get("items", [])
#         total = sum([float(item["quantity"]) * float(item["price"]) for item in items])

#         serializer.save(invoice_number=invoice_number, total=total)


# class InvoiceDetailView(generics.RetrieveAPIView):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     lookup_field = "id"
