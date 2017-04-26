from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from fitting.models import Scan, User
from .utils import update_foot_scans
import logging
from web.settings import str2bool

logger = logging.getLogger(__name__)

update_scan_functions = {
    'foot': update_foot_scans
}


@csrf_exempt
@transaction.atomic
def update_scan_view(request):
    user_uuid = request.GET['user']
    scanner = request.GET['scanner']
    scan_id = request.GET['scan']
    scan_type = request.GET['type']
    try:
        is_scan_default = str2bool(request.GET['is_default'])
    except MultiValueDictKeyError:
        is_scan_default = False

    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        user = User(uuid=user_uuid)
        user.save()
    try:
        scans = update_scan(user, scanner, scan_id, scan_type, request.build_absolute_uri)
    except ValueError:
        return HttpResponseBadRequest()

    if is_scan_default or not user.default_scans.all().exists():
        for scan in scans:
            user.default_scans.add(scan)
        user.save()

    return HttpResponse(
        json.dumps([str(scan) for scan in scans])
    )


@transaction.atomic
def update_scan(user, scanner, scan_id, scan_type, absolute_uri_builder):

    result = update_scan_functions[scan_type](user, scanner, scan_id, scan_type, absolute_uri_builder)
    return result if isinstance(result, list) else list(result)

