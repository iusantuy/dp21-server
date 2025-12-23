from decimal import Decimal
from datetime import date
from invoice.domain.entities import InvoiceEntity, InvoiceItemEntity

def test_invoice_item_total_price():
    item = InvoiceItemEntity(description="Croissant", quantity=2, unit_price=Decimal("25000"))
    assert item.total_price == Decimal("50000")

def test_invoice_total_amount():
    items = [
        InvoiceItemEntity(description="Croissant", quantity=2, unit_price=Decimal("25000")),
        InvoiceItemEntity(description="Baguette", quantity=1, unit_price=Decimal("30000")),
    ]
    invoice = InvoiceEntity(
        id=1,
        customer_name="John Doe",
        customer_email="john@example.com",
        date_created=date.today(),
        due_date=date.today(),
        total_amount=Decimal("0"),
        items=items
    )
    
    total = sum(item.total_price for item in items)
    assert total == Decimal("80000")
