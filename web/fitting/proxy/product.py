from django import forms
from django.contrib.admin.options import TabularInline
from ..models import Product, LastAttribute, ModelType, Size, CompareResult
from .last import LastProxy
from .base_models_admin import BaseModelAdmin
from django.db import transaction
import json
import csv
import os


class ProductProxy(Product):

    class Meta:
        proxy = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    @transaction.atomic
    def create_attribute(self, size, scan_attribute_name, name, value, ranges, last_type):

        last = LastProxy.objects.filter(product__uuid=self.uuid, size__value=size, model_type=last_type).first()
        if last is None:
            product_obj = Product.objects.get(uuid=self)
            size_obj = Size.objects.get(model_type=ModelType.TYPE_FOOT, value=size)
            last = LastProxy(product=product_obj, size=size_obj, model_type=last_type)
            last.save()

        attribute = LastAttribute.objects.filter(
            last=last,
            name=name,
        ).last()
        if attribute is None:
            attribute = LastAttribute(
                last=last,
                name=name,
            )
        attribute.scan_attribute_name = scan_attribute_name
        attribute.value = value.replace(',', '.')
        attribute.disabled = True if scan_attribute_name == '' else False
        if not attribute.disabled:
            attribute.left_limit_value = ranges[0]
            attribute.best_value = ranges[1]
            attribute.right_limit_value = ranges[2]

        attribute.save()

    def save(self, *args, **kwargs):
        old_product = ProductProxy.objects.get(pk=self.pk)
        if self.attachment != old_product.attachment:
            with open(self.attachment.path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')

                for row in reader:
                    self.create_attribute(row['size'], row['scan_metric'], row['last_metric'], row['value'], (row['l_f1'], row['l_shift'], row['l_f2']), ModelType.TYPE_LEFT_FOOT)
                    self.create_attribute(row['size'], row['scan_metric'], row['last_metric'], row['value'], (row['r_f1'], row['r_shift'], row['r_f2']), ModelType.TYPE_RIGHT_FOOT)

            CompareResult.objects.filter(last__product=self).delete()
        super(ProductProxy, self).save(*args, **kwargs)


class ProductLastInline(TabularInline):

    model = LastProxy
    can_delete = True
    extra = 1

    class Meta:
        model = LastProxy
        fields = [
            'id',
            'size',
            'path',
            'attachment',
        ]


class ProductAdmin(BaseModelAdmin):

    fields = [
        'uuid',
        'brand_id',
        'attachment',
    ]

    readonly_fields = [
    ]

    list_display = [
        'uuid',
        'brand_id',
        'attachment',
    ]

    search_fields = (
        'uuid',
        'brand_id',
    )

    inlines = [
        ProductLastInline
    ]

