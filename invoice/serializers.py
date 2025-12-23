# invoices/serializers.py
from rest_framework import serializers
from .infrastructure.models import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ["id", "name", "quantity", "price", "subtotal"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "store_name",
            "store_address",
            "customer_name",
            "customer_address",
            "date",
            "notes",
            "total",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice
