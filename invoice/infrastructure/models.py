from django.db import models
from decimal import Decimal

from invoice.domain.entities import InvoiceEntity, InvoiceItemEntity

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    due_date = models.DateField(null=True, blank=True)
    to = models.CharField(max_length=255)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dp = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    @property
    def items_total(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0"))

    def recalculate_total(self):
        self.total = self.items_total - self.dp
        self.save(update_fields=["total"])

    # <-- ini yang harus lo tambahin
    def to_entity(self) -> InvoiceEntity:
        items = [
            InvoiceItemEntity(
                name=i.name,  # entity pakai description
                quantity=i.quantity,
                price=i.price,
                subtotal=i.subtotal
            )
            for i in self.items.all()
        ]
        entity = InvoiceEntity(
            id=self.id,
            invoice_number=self.invoice_number,
            due_date=self.due_date,
            to=self.to,
            date_created=self.date_created,
            items=items,
            notes=self.notes,
            _total=self.total,
        )
        entity.calculate_total()
        return entity

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    @property
    def subtotal(self):
        return Decimal(self.quantity) * self.price

