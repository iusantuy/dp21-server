import pytest
from decimal import Decimal
from invoice.application.services.invoice_service import InvoiceService
from invoice.infrastructure.models import Invoice

@pytest.mark.django_db(transaction=True)
def test_invoice_service_creates_invoice_and_items():
    service = InvoiceService()
    data = {
        "invoice_number": "INV-TEST-001",
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

    invoice = service.create_invoice(data)
    
    db_invoice = Invoice.objects.get(invoice_number="INV-TEST-001")
    assert db_invoice.total == Decimal("80000")
    assert db_invoice.items.count() == 2
