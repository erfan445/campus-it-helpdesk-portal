from django.contrib import admin
from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'name', 'category', 'status', 'assigned_to', 'location', 'warranty_expiry')
    list_filter = ('category', 'status', 'location')
    search_fields = ('asset_tag', 'name', 'serial_number', 'assigned_to__username', 'location')
