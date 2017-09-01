from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from fitting.models import Scan, User, ModelType, Product, ScanAttribute
from .utils import update_foot_scans, CompareScansThread, set_default_scan
import logging
from web.settings import str2bool
import sys, traceback

logger = logging.getLogger(__name__)

update_scan_functions = {
    ModelType.TYPE_FOOT: update_foot_scans
}


@csrf_exempt
def update_scan_view(request):
    user_uuid = request.GET['user']
    scanner = request.GET['scanner']
    scan_id = request.GET['scan']
    scan_type = request.GET.get('type', ModelType.TYPE_FOOT).upper()
    is_scan_default = str2bool(request.GET.get('is_default', 'false'))
    brand_id = request.GET.get('brand', None)

    user = User.objects.filter(uuid=user_uuid).first()
    if user is None:
        user = User(uuid=user_uuid)
        user.save()
    try:
        scans = update_scan(user, scanner, scan_id, scan_type)
        for scan in scans:
            products = Product.objects.filter(brand_id=int(brand_id)) if brand_id else Product.objects.all()
            CompareScansThread(scan, products).start()
    except ValueError:
        logger.debug(f'scan {scan_id} desn`t update')
        traceback.print_exc(file=sys.stdout)
        return HttpResponseBadRequest()

    if is_scan_default or not user.default_scans.all().exists():
        for scan in scans:
            set_default_scan(user, scan)
        

    return HttpResponse(
        json.dumps([str(scan) for scan in scans])
    )


def update_scan(user, scanner, scan_id, scan_type):

    result = update_scan_functions[scan_type](user, scanner, scan_id, scan_type)
    return result if isinstance(result, list) else list(result)

