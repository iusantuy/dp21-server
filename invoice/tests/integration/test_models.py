import pytest
from decimal import Decimal
from datetime import date
from invoice.infrastructure.models import Invoice, InvoiceItem
from invoice.application.services.invoice_service import InvoiceService
from django.db import IntegrityError

@pytest.mark.django_db
def test_invoice_model_create_and_str():
    """Test basic Invoice creation and __str__"""
    invoice = Invoice.objects.create(
        invoice_number="INV-001",
        store_name="My Bakery",
        store_address="Jl. Mawar No.5",
        customer_name="John Doe",
        customer_address="Jl. Melati No.10",
        total=Decimal("50000")
    )
    assert str(invoice) == "INV-001"


@pytest.mark.django_db
def test_invoice_item_model_create_and_subtotal():
    """Test basic InvoiceItem creation and subtotal calculation"""
    invoice = Invoice.objects.create(
        invoice_number="INV-002",
        store_name="My Bakery",
        store_address="Jl. Mawar No.5",
        customer_name="John Doe",
        customer_address="Jl. Melati No.10",
        total=Decimal("0")
    )
    item = InvoiceItem.objects.create(invoice=invoice, name="Croissant", quantity=2, price=25000)
    assert item.subtotal == 50000


@pytest.mark.django_db
def test_create_invoice_atomic():
    """Test creating invoice + items via service layer, total calculation, atomic save"""
    data = {
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

    invoice = InvoiceService.create_invoice(data)

    # Cek DB
    assert Invoice.objects.count() == 1
    assert InvoiceItem.objects.count() == 2
    assert invoice.total == 80000


@pytest.mark.django_db
def test_atomic_rollback_on_error():
    """Test rollback when invalid data occurs"""
    data = {
        "store_name": "My Bakery",
        "store_address": "Jl. Mawar No.5",
        "customer_name": "John Doe",
        "customer_address": "Jl. Melati No.10",
        "due_date": "2025-11-10",
        "notes": "Terima kasih",
        "items": [
            {"name": "Croissant", "quantity": 2, "price": 25000},
            {"name": "Baguette", "quantity": 1, "price": 30000},
            {"name": "", "quantity": 1, "price": 10000}  # Invalid name, should trigger error
        ]
    }

    with pytest.raises(Exception):
        InvoiceService.create_invoice(data)

    # Pastikan rollback, DB tetap bersih
    assert Invoice.objects.count() == 0
    assert InvoiceItem.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity,price,expected",
    [
        (0, 25000, 0),           # quantity zero
        (2, 0, 0),               # price zero
        (3, 10000, 30000),       # normal case
        (1, -5000, -5000),       # negative price
    ]
)
def test_invoice_item_subtotal_edge_cases(quantity, price, expected):
    """Test edge cases for InvoiceItem subtotal"""
    invoice = Invoice.objects.create(
        invoice_number="INV-EDGE",
        store_name="Edge Bakery",
        store_address="Jl. Edge No.1",
        customer_name="Edge Tester",
        customer_address="Jl. Edge No.2",
        total=Decimal("0")
    )
    item = InvoiceItem.objects.create(invoice=invoice, name="Test Item", quantity=quantity, price=price)
    assert item.subtotal == expected








# import pytest
# from invoices.infrastructure.models import Invoice, InvoiceItem
# from invoices.application.services.invoice_service import InvoiceService

# @pytest.mark.django_db
# def test_create_invoice_atomic():
#     data = {
#         "store_name": "My Bakery",
#         "store_address": "Jl. Mawar No.5",
#         "customer_name": "John Doe",
#         "customer_address": "Jl. Melati No.10",
#         "due_date": "2025-11-10",
#         "notes": "Terima kasih",
#         "items": [
#             {"name": "Croissant", "quantity": 2, "price": 25000},
#             {"name": "Baguette", "quantity": 1, "price": 30000}
#         ]
#     }

#     invoice = InvoiceService.create_invoice(data)

#     # Pastikan invoice tersimpan di DB
#     assert Invoice.objects.count() == 1
#     assert InvoiceItem.objects.count() == 2
#     assert invoice.total == 80000

# @pytest.mark.django_db
# def test_atomic_rollback_on_error():
#     from django.db import IntegrityError

#     data = {
#         "store_name": "My Bakery",
#         "store_address": "Jl. Mawar No.5",
#         "customer_name": "John Doe",
#         "customer_address": "Jl. Melati No.10",
#         "due_date": "2025-11-10",
#         "notes": "Terima kasih",
#         "items": [
#             {"name": "Croissant", "quantity": 2, "price": 25000},
#             {"name": "Baguette", "quantity": 1, "price": 30000},
#             {"name": "", "quantity": 1, "price": 10000},  # Invalid name
#         ]
#     }

#     with pytest.raises(Exception):
#         InvoiceService.create_invoice(data)

#     # Pastikan rollback, tidak ada invoice tersimpan
#     assert Invoice.objects.count() == 0
#     assert InvoiceItem.objects.count() == 0




# import pytest
# from decimal import Decimal
# from invoices.infrastructure.models import Invoice, InvoiceItem

# @pytest.mark.django_db
# def test_invoice_model_create_and_str():
#     invoice = Invoice.objects.create(
#         invoice_number="INV-001",
#         store_name="My Bakery",
#         store_address="Jl. Mawar No.5",
#         customer_name="John Doe",
#         customer_address="Jl. Melati No.10",
#         total=Decimal("50000")
#     )
#     assert str(invoice) == "INV-001"

# @pytest.mark.django_db
# def test_invoice_item_model_create_and_subtotal():
#     invoice = Invoice.objects.create(
#         invoice_number="INV-002",
#         store_name="My Bakery",
#         store_address="Jl. Mawar No.5",
#         customer_name="John Doe",
#         customer_address="Jl. Melati No.10",
#         total=Decimal("0")
#     )
#     item = InvoiceItem.objects.create(invoice=invoice, name="Croissant", quantity=2, price=25000)
#     assert item.subtotal == 50000
