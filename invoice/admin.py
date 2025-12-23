from django.contrib import admin
from .infrastructure.models import Invoice

# Register your models here.
admin.site.register(Invoice)