from django.contrib.admin.options import TabularInline
from ..models import Product, Last
from .base_models_admin import BaseModelAdmin


class ProductProxy(Product):

    class Meta:
        proxy = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductLastInline(TabularInline):

    model = Last
    can_delete = True
    extra = 1

    class Meta:
        model = Last
        fields = [
            'id',
            'size',
            'path',
            'attachment',
        ]


class ProductAdmin(BaseModelAdmin):

    fields = [
        'uuid',
    ]

    readonly_fields = [
    ]

    list_display = [
        'uuid',
    ]

    search_fields = (
        'uuid',
    )

    inlines = [
        ProductLastInline
    ]

