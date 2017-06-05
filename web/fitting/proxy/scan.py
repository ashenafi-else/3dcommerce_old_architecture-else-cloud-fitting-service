from django.contrib.admin.options import TabularInline
from ..models import ScanAttribute, Scan
from .base_models_admin import BaseModelAdmin


class ScanProxy(Scan):

    class Meta:
        proxy = True
        verbose_name = 'Scan'
        verbose_name_plural = 'Scans'


class ScanAttributesInline(TabularInline):

    model = ScanAttribute
    extra = 1

    fields = [
        'name',
        'value',
    ]

    list_display = [
        'name',
        'value',
    ]

    readonly_fields = [
        'name',
        'value',
    ]


class ScanAdmin(BaseModelAdmin):

    fields = [
        'user',
        'scan_id',
        'scanner',
        'model_type',
        'attachment',
        'created_date',
    ]

    readonly_fields = [
        'created_date',
    ]

    list_display = [
        'user',
        'scan_id',
        'scanner',
        'model_type',
        'attachment',
        'created_date',
    ]

    search_fields = (
        'user',
        'scan_id',
        'scanner',
        'model_type',
        'attachment',
        'created_date',
    )

    inlines = [
        ScanAttributesInline
    ]
