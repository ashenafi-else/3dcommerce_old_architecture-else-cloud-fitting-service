from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from fitting.models import Scan, User, ModelType, Product, ScanAttribute
from .utils import update_foot_scans, compare_by_metrics, set_default_scan, VisualisationThread, get_last_scan_id
from web.settings import str2bool

import logging
import json

logger = logging.getLogger(__name__)

update_scan_functions = {
    ModelType.TYPE_FOOT: update_foot_scans
}


@csrf_exempt
def update_last_scan_view(request):
    user_uuid = request.GET['user']
    scanner = request.GET['scanner']
    interval = int(request.GET['time'])
    scan_type = request.GET.get('type', ModelType.TYPE_FOOT).upper()
    is_scan_default = str2bool(request.GET.get('is_default', 'false'))
    brand_id = request.GET.get('brand', None)

    user = User.objects.filter(uuid=user_uuid).first()
    if user is None:
        user = User(uuid=user_uuid)
        user.save()
    scan_id = get_last_scan_id(user, scanner, interval)
    if scan_id is None:
        return HttpResponseNotFound(json.dumps({'error': 'scan by given interval does not exist.'}))
    scans = update_scan(user, scanner, scan_id, scan_type)
    if len(scans) == 0:
        return HttpResponseNotFound(json.dumps({'error': 'scan is not found.'}))
    try:
        for scan in scans:
            products = Product.objects.filter(brand_id=int(brand_id)) if brand_id else Product.objects.all()
            for product in products:
                compare_by_metrics(scan, product)
    except Exception as e:
        logger.error(f'scan {scan_id} desn`t compare')
        traceback.print_exc(file=sys.stdout)
    products = Product.objects.filter(brand_id=int(brand_id)) if brand_id else Product.objects.all()
    VisualisationThread(scans[0], scans[1], products).start()
        

    if is_scan_default or not user.default_scans.all().exists():
        for scan in scans:
            set_default_scan(user, scan)
        

    return HttpResponse(
        json.dumps([str(scan) for scan in scans])
    )

def update_scan(user, scanner, scan_id, scan_type):

    result = update_scan_functions[scan_type](user, scanner, scan_id, scan_type)
    return result if isinstance(result, list) else list(result)

