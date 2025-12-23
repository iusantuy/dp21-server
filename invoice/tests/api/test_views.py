import pytest
from rest_framework.test import APIClient
from invoice.infrastructure.models import Invoice

@pytest.mark.django_db
def test_create_invoice_api():
    client = APIClient()
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

    response = client.post("/api/invoices/", data, format="json")

    assert response.status_code == 201
    assert response.data["total"] == 80000
    assert Invoice.objects.count() == 1
