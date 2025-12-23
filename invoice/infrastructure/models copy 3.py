from django.db import models
from decimal import Decimal

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    due_date = models.DateField(null=True, blank=True)
    to = models.CharField(max_length=255)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dp = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    notes = models.TextField(blank=True, default="")   # FIX

    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    @property
    def items_total(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0"))

    def recalculate_total(self):
        self.total = self.items_total - self.dp
        self.save(update_fields=["total"])

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)    # FIX: rename menu → name
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    @property
    def subtotal(self):
        return Decimal(self.quantity) * self.price
