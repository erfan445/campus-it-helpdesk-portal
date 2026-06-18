from django.conf import settings
from django.db import models


class Asset(models.Model):
    class Category(models.TextChoices):
        LAPTOP = 'LAPTOP', 'Laptop'
        DESKTOP = 'DESKTOP', 'Desktop'
        PRINTER = 'PRINTER', 'Printer'
        NETWORK = 'NETWORK', 'Network Device'
        PHONE = 'PHONE', 'Phone'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        IN_REPAIR = 'IN_REPAIR', 'In Repair'
        SPARE = 'SPARE', 'Spare'
        RETIRED = 'RETIRED', 'Retired'
        LOST = 'LOST', 'Lost'

    asset_tag = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    serial_number = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['asset_tag']

    def __str__(self):
        return f'{self.asset_tag} - {self.name}'
