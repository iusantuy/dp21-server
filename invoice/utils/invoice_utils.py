def generate_invoice_number(customer_name: str) -> str:
    """
    Generate invoice number format: "XX/DCP/MM/YY"
    XX = urutan invoice untuk customer ini (2 digit)
    """
    MONTH_ORDER = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }
    from django.utils import timezone
    from ..infrastructure.models import Invoice

    today = timezone.now()
    month = today.month
    year = today.year % 100

    # Standarisasi nama customer agar case-insensitive
    customer = customer_name.strip().title()

    # Hitung jumlah invoice yang sudah ada untuk pelanggan ini
    invoice_count = Invoice.objects.filter(to__iexact=customer).count()  # <-- iexact biar case-insensitive

    # Urutan invoice baru = count existing + 1
    order_number = str(invoice_count + 1).zfill(2)

    month_order_no = MONTH_ORDER[month]
    return f"{order_number}/DCP/{month_order_no}/{year}"
