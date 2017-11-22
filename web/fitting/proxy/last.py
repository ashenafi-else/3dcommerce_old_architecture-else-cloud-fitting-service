from django.contrib.admin.options import TabularInline
from ..models import LastAttribute, Last, CompareResult, CompareVisualization
from .base_models_admin import BaseModelAdmin
from django.utils.html import format_html
from django.urls import reverse


class LastProxy(Last):

    class Meta:
        proxy = True
        verbose_name = 'Last'
        verbose_name_plural = 'Lasts'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_last = LastProxy.objects.get(pk=self.pk)
            if old_last.attachment != self.attachment:
                CompareVisualization.objects.filter(last=self).delete()
        super(LastProxy, self).save(*args, **kwargs)
        CompareResult.objects.filter(last__product=self.product).delete()


class LastAttributesInline(TabularInline):

    model = LastAttribute
    can_delete = True
    extra = 1

    class Meta:
        model = Last
        fields = [
            'name',
            'value',
            'left_limit_value',
            'best_value',
            'right_limit_value',
            'disabled',
        ]


class LastAdmin(BaseModelAdmin):

    def workflow(self, obj):
        link = '<a href="{}?increment_size=true">{}</a>'.format(reverse('copy_last', args=(obj.pk,)), 'Copy and incremet size')
        return format_html(
            '<span>'+link+'</span>'
        )
    workflow.boolean = False
    workflow.short_description = 'Action'

    fields = [
        'workflow',
        'product',
        'size',
        'attachment',
        'model_type',
    ]

    readonly_fields = [
        'workflow'
    ]

    list_display = [
        'product',
        'size',
        'model_type',
        'attachment',
        'workflow',
    ]

    search_fields = (
        'product__uuid',
        'size__value',
        'model_type',
    )

    inlines = [
        LastAttributesInline
    ]

