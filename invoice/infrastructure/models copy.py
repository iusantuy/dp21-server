# invoices/infrastructure/models.py
from django.db import models
from decimal import Decimal
from invoice.domain.entities import InvoiceEntity, InvoiceItemEntity


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    store_name = models.CharField(max_length=255)
    store_address = models.TextField()
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.invoice_number

    @property
    def items_total(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0.00"))

    def recalculate_total(self):
        self.total = self.items_total
        self.save(update_fields=["total"])

    def to_entity(self) -> InvoiceEntity:
        items = [
            InvoiceItemEntity(
                description=i.name,
                quantity=i.quantity,
                unit_price=i.price,
            )
            for i in self.items.all()
        ]
        entity = InvoiceEntity(
            id=self.id,
            invoice_number=self.invoice_number,
            store_name=self.store_name,
            store_address=self.store_address,
            customer_name=self.customer_name,
            customer_address=self.customer_address,
            date_created=self.date_created,
            due_date=self.due_date,
            items=items,
            notes=self.notes,
            total_amount=self.total,
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
        return self.quantity * self.price










# # invoices/models.py
# from django.db import models

# class Invoice(models.Model):
#     invoice_number = models.CharField(max_length=50, unique=True)
#     store_name = models.CharField(max_length=255)
#     store_address = models.TextField()
#     customer_name = models.CharField(max_length=255)
#     customer_address = models.TextField()
#     date = models.DateField(auto_now_add=True)
#     notes = models.TextField(blank=True)
#     total = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return self.invoice_number


# class InvoiceItem(models.Model):
#     invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return f"{self.name} ({self.quantity})"

#     @property
#     def subtotal(self):
#         return self.quantity * self.price
