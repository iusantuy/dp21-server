# invoices/application/services/invoice_service.py
from django.db import transaction
from decimal import Decimal
from invoice.infrastructure.models import Invoice, InvoiceItem
from invoice.utils.invoice_utils import generate_invoice_number


class InvoiceService:
    @staticmethod
    @transaction.atomic
    def create_invoice(data):
        """
        Buat invoice baru + item + hitung total.
        data contoh:
        {
          "invoice_number": "INV-001",
          "store_name": "My Bakery",
          "store_address": "Jl. Mawar No.5",
          "customer_name": "John Doe",
          "customer_address": "Jl. Melati No.10",
          "due_date": "2025-11-10",
          "notes": "Terima kasih",
          "items": [
              {"name": "Croissant", "quantity": 2, "price": 25000},
              {"name": "Baguette", "quantity": 1, "price": 30000}
          ]
        }
        """
        customer_name = data.get("to")
        invoice_number = generate_invoice_number(customer_name)
        items_data = data.pop("items", [])
        invoice = Invoice.objects.create(
            invoice_number = invoice_number,
            **data,
            total=Decimal("0.00"),
        )

        total = Decimal("0.00")
        for item in items_data:
            subtotal = Decimal(item["price"]) * int(item["quantity"])
            InvoiceItem.objects.create(
                invoice=invoice,
                name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )
            total += subtotal

        invoice.total = total
        invoice.save(update_fields=["total"])

        return invoice.to_entity()
    

















