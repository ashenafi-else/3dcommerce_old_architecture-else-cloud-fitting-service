from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from fitting.models import Scan, User, ScanAttribute, ModelType
from .utils.update_scan import update_scan
import logging
import json

logger = logging.getLogger(__name__)


urls_to_scans = {
    ModelType.TYPE_LEFT_FOOT: lambda url, scanner, scan_id: f'{url}/{scanner}/{scan_id}/model_l.stl',
    ModelType.TYPE_RIGHT_FOOT: lambda url, scanner, scan_id: f'{url}/{scanner}/{scan_id}/model_r.stl',
}


@csrf_exempt
def update_all_scans(request):

    scans = Scan.objects.all()
    not_updated = []
    for scan in scans:
        try:
            user = scan.user
            update_scan(
                user=user,
                scanner=scan.scanner,
                scan_id=scan.scan_id,
                scan_type=scan.model_type,
                scan_path=urls_to_scans[scan.model_type](user.base_url, scan.scanner, scan.scan_id)
            )
        except (User.DoesNotExist, ValueError):
            logger.debug('scan {} does not update!'.format(scan))
            not_updated.append(str(scan))
    return HttpResponse(json.dumps({'not_updated': not_updated}))