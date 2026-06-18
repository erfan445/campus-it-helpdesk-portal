from django.db.models import Count
from .models import Asset


def asset_summary():
    return {
        'total_assets': Asset.objects.count(),
        'active_assets': Asset.objects.filter(status=Asset.Status.ACTIVE).count(),
        'repair_assets': Asset.objects.filter(status=Asset.Status.IN_REPAIR).count(),
        'by_category': Asset.objects.values('category').annotate(total=Count('id')).order_by('category'),
    }
