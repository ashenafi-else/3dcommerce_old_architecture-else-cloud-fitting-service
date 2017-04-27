from django.contrib.admin.options import TabularInline
from ..models import LastAttribute, Last
from .base_models_admin import BaseModelAdmin


class LastProxy(Last):

    class Meta:
        proxy = True
        verbose_name = 'Last'
        verbose_name_plural = 'Lasts'


class LastAttributesInline(TabularInline):

    model = LastAttribute
    can_delete = True
    extra = 1

    class Meta:
        model = Last
        fields = [
            'name',
            'value',
        ]


class LastAdmin(BaseModelAdmin):

    fields = [
        'product',
        'size',
    ]

    readonly_fields = [
    ]

    list_display = [
        'product',
        'size',
    ]

    search_fields = (
        'product',
        'size',
    )

    inlines = [
        LastAttributesInline
    ]

