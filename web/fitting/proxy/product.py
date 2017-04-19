from django.contrib.admin.options import TabularInline
from fitting.models import Product, Last
from common.proxy.base_models_admin import BaseModelAdmin


class ProductProxy(Product):

	class Meta:
		proxy = True
		verbose_name = 'Product lasts'
        verbose_name_plural = 'Product lasts'


class ProductLastProxy(Last):

    class Meta:
        proxy = True
        verbose_name = 'Product'
        verbose_name_plural = 'Product'


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
        'id',
        'uuid',
    ]

    readonly_fields = [
    ]

    list_display = [
        'id',
        'uuid',
    ]

    search_fields = (
        'uuid',
    )

    inlines = [
        LastInline
    ]

