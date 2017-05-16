from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from fitting.models import Scan, User
from .utils import set_default_scan
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def set_default_scan_view(request):
    user_uuid = request.GET['user']
    scan_id = request.GET['scan']
    
    user = User.objects.get(uuid=user_uuid)
    scans = Scan.objects.filter(user=user, scan_id=scan_id)
    for scan in scans:
        set_default_scan(user, scan)
        
    return HttpResponse(
        json.dumps([str(scan) for scan in scans])
    )
