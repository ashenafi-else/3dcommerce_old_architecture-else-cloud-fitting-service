from django.http.response import HttpResponseRedirect
from django.urls import reverse

from fitting.models import Last, LastAttribute, Size
from web.settings import str2bool


def copy_last(request, pk):

    is_increment = str2bool(request.GET.get('increment_size', False))

    last = Last.objects.filter(pk=pk).first()
    attributes = LastAttribute.objects.filter(last=last)

    last.pk = None
    if is_increment:
        size = Size.objects.filter(numeric_value=last.size.numeric_value + 1, model_type=last.size.model_type).first()
        if Size is not None:
            last.size = size
    last.save()

    for attribute in attributes:
    	attribute.pk = None
    	attribute.last = last
    	attribute.save()

    return HttpResponseRedirect(
        reverse('admin:fitting_lastproxy_change', args=(last.pk,))
    )
