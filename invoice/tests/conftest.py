import pytest
from decimal import Decimal
from datetime import date
from invoice.domain.entities import InvoiceEntity, InvoiceItemEntity
from invoice.infrastructure.models import Invoice, InvoiceItem
from django.contrib.auth.models import User

@pytest.fixture
def sample_invoice_items():
    return [
        InvoiceItemEntity(description="Croissant", quantity=2, unit_price=Decimal("25000")),
        InvoiceItemEntity(description="Baguette", quantity=1, unit_price=Decimal("30000")),
    ]

@pytest.fixture
def sample_invoice_entity(sample_invoice_items):
    return InvoiceEntity(
        id=1,
        customer_name="John Doe",
        customer_email="john@example.com",
        date_created=date.today(),
        due_date=date.today(),
        total_amount=Decimal("0"),
        items=sample_invoice_items
    )

@pytest.fixture
def sample_user(db):
    return User.objects.create_user(username="testuser", password="password")
