from django.test import TestCase
from apps.assets.models import Asset


class AssetModelTests(TestCase):
    def test_asset_string_contains_tag_and_name(self):
        asset = Asset.objects.create(asset_tag='EMU-LAP-001', name='Dell Latitude')
        self.assertEqual(str(asset), 'EMU-LAP-001 - Dell Latitude')
