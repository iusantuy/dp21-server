# invoices/domain/entities.py
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class InvoiceItemEntity:
    name: str
    quantity: int
    price: Decimal
    subtotal: Decimal
    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.price


@dataclass
class InvoiceEntity:
    id: int
    invoice_number: str
    due_date: date
    to: str
    # store_name: str
    # store_address: str
    # customer_name: str
    # customer_address: str
    items: List[InvoiceItemEntity] = field(default_factory=list)
    _total: Decimal = Decimal("0.00")
    notes: str = ""
    date_created: date = field(default_factory=date.today)

    @property
    def total(self):
        return self._total

    def calculate_total(self):
        """Hitung total dari semua items"""
        self._total = sum(
            (item.total_price for item in self.items), Decimal("0.00")
        )
        return self.total








# from dataclasses import dataclass
# from datetime import date
# from decimal import Decimal
# from typing import List

# @dataclass
# class InvoiceItemEntity:
#     description: str
#     quantity: str
#     unit_price: Decimal

#     @property
#     def total_price(self) -> Decimal:
#         self.quantity * self.unit_price

# @dataclass
# class InvoiceEntity:
#     id: int
#     customer_name: str
#     customer_email: str
#     date_created: date
#     due_date: date
#     total_amount: Decimal
#     items: List[InvoiceItemEntity]