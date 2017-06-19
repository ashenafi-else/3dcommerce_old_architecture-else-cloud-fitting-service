from django.http.response import HttpResponseRedirect
from django.urls import reverse

from fitting.models import Last, LastAttribute


def copy_last(request, pk):
    last = Last.objects.filter(pk=pk).first()
    attributes = LastAttribute.objects.filter(last=last)

    last.pk = None
    last.save()

    for attribute in attributes:
    	attribute.pk = None
    	attribute.last = last
    	attribute.save()

    return HttpResponseRedirect(
        reverse('admin:fitting_lastproxy_change', args=(last.pk,))
    )
