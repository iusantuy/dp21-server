# invoices/presentation/serializers.py
from rest_framework import serializers
from invoice.infrastructure.models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["name", "quantity", "price"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "store_name",
            "store_address",
            "customer_name",
            "customer_address",
            "due_date",
            "notes",
            "items",
        ]


class InvoiceResponseItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)


class InvoiceResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    invoice_number = serializers.CharField()
    customer_name = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    date_created = serializers.DateField()
    items = InvoiceResponseItemSerializer(many=True)







# # invoices/presentation/serializers.py
# from rest_framework import serializers


# class InvoiceItemSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     quantity = serializers.IntegerField(min_value=1)
#     price = serializers.DecimalField(max_digits=12, decimal_places=2)


# class InvoiceCreateSerializer(serializers.Serializer):
#     invoice_number = serializers.CharField(max_length=50)
#     store_name = serializers.CharField(max_length=255)
#     store_address = serializers.CharField()
#     customer_name = serializers.CharField(max_length=255)
#     customer_address = serializers.CharField()
#     due_date = serializers.DateField()
#     notes = serializers.CharField(allow_blank=True, required=False)
#     items = InvoiceItemSerializer(many=True)


# class InvoiceResponseSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     invoice_number = serializers.CharField()
#     customer_name = serializers.CharField()
#     total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
#     date_created = serializers.DateField()
