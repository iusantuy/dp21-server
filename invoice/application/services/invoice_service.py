from django.db import transaction
from decimal import Decimal
from invoice.infrastructure.models import Invoice, InvoiceItem


class InvoiceService:
    @staticmethod
    @transaction.atomic
    def create_invoice(data):
        """
        Buat invoice baru + item + hitung total.
        data sudah mengandung:
        - invoice_number (sudah diset di views)
        - due_date
        - to
        - dp
        - notes
        - items
        """

        items_data = data.pop("items", [])
        dp = Decimal(str(data.get("dp", 0)))  # pastiin decimal aman

        # Invoice utama
        invoice = Invoice.objects.create(
            total=Decimal("0.00"),
            **data,
        )

        subtotal = Decimal("0.00")

        for item in items_data:
            price = Decimal(str(item["price"]))
            qty = int(item["quantity"])
            sub = price * qty

            InvoiceItem.objects.create(
                invoice=invoice,
                name=item["name"],
                quantity=qty,
                price=price,
            )

            subtotal += sub

        # Total = Subtotal - DP
        total_final = subtotal - dp

        invoice.subtotal = subtotal
        invoice.total = total_final
        invoice.save(update_fields=["subtotal", "total"])

        return invoice.to_entity()
