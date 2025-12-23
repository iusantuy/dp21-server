from django.utils import timezone
from ..infrastructure.models import Invoice
import json

def generate_invoice_number(customer_name: str) -> str:
    """
    Generate invoice number format: "XX/DCP/MM/YY"
    XX      = urutan invoice untuk customer ini (2 digit)
    """
    MONTH_ORDER = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }
    from django.utils import timezone
    today = timezone.now()
    month = today.month
    year = today.year % 100
    customer = customer_name.strip().title()

    # cek jumlah invoice yang sudah ada untuk pelanggan ini
    # untuk preview, kita bisa include juga data draft (opsional)
    invoice_count = Invoice.objects.filter(to=customer).count()
    order_number = str(invoice_count + 1).zfill(2)
    month_order_no = MONTH_ORDER[month]
    return f"{order_number}/DCP/{month_order_no}/{year}"
