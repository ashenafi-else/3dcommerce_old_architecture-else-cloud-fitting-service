from django.contrib.admin.options import TabularInline
from ..models import LastAttribute, Last , Size
from .base_models_admin import BaseModelAdmin


class LastAttributeProxy(LastAttribute):

    class Meta:
        proxy = True
        verbose_name = 'Last Attribute'
        verbose_name_plural = 'Last Attributes'


class LastAttributeAdmin(BaseModelAdmin):

    fields = [
        'last',
        'name',
        'value',
        'left_limit_value',
        'best_value',
        'right_limit_value',
        'disabled',
    ]

    readonly_fields = [
    ]

    list_filter = [
        'name',
    ]

    list_display = [
        'last',
        'value',
        'left_limit_value',
        'best_value',
        'right_limit_value',
        'disabled',
    ]

    list_editable = [
        'value',
        'left_limit_value',
        'best_value',
        'right_limit_value',
        'disabled',
    ]

