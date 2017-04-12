from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, Shoe, User, Attribute
from .update_user_foot_scan import update_scan
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def update_all_scans(request):

    scans = Scan.objects.all()
    not_updated = []
    for scan in scans:
        try:
            user = User.objects.get(id=scan.user_id)
            update_scan(user, scan.scanner, scan.scan_id, scan.type)
        except (User.DoesNotExist, ValueError):
            logger.debug('scan {} does not update!'.format(scan.id))
            not_updated.append(scan.id)
    return HttpResponse(json.dumps({'not_updated': not_updated}))