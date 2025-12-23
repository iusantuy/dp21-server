# invoices/domain/entities.py
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class InvoiceItemEntity:
    name: str
    quantity: int
    unit_price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.unit_price


@dataclass
class InvoiceEntity:
    id: int
    invoice_number: str
    due_date: date
    to: str
    date_created: date
    # store_name: str
    # store_address: str
    # customer_name: str
    # customer_address: str
    items: List[InvoiceItemEntity] = field(default_factory=list)
    notes: str = ""
    total_amount: Decimal = Decimal("0.00")

    @property
    def total(self):
        return self.total_amount

    def calculate_total(self):
        """Hitung total dari semua items"""
        self.total_amount = sum(
            (item.total_price for item in self.items), Decimal("0.00")
        )
        return self.total_amount








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