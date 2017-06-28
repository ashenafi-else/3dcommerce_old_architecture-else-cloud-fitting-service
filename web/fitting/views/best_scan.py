from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from fitting.models import User, Scan, ModelType, ScanAttribute
from fitting_algorithm import get_best_scan
import json
import logging

logger = logging.getLogger(__name__)


def extract_calculation_attributes(attributes):
    attrs = {}
    for atr in attributes:
        try:
            attrs[atr.name] = float(atr.value)
        except ValueError:
            False

    return attrs


def get_best_foot_scan(user):

    scans_data = {}
    scans = Scan.objects.filter(Q(model_type=ModelType.TYPE_LEFT_FOOT) | Q(model_type=ModelType.TYPE_RIGHT_FOOT), user=user,)

    for scan in scans:
        scan_attributes = ScanAttribute.objects.filter(scan=scan.id)
        if not scan.scan_id in scans_data:
            scans_data[scan.scan_id] = {}

        if scan.model_type == ModelType.TYPE_LEFT_FOOT:
            scans_data[scan.scan_id]['LEFT'] = extract_calculation_attributes(scan_attributes)
        elif scan.model_type == ModelType.TYPE_RIGHT_FOOT:
            scans_data[scan.scan_id]['RIGHT'] = extract_calculation_attributes(scan_attributes)

    return get_best_scan(scans_data)


find_best_scan = {
    ModelType.TYPE_FOOT: get_best_foot_scan
}


@csrf_exempt
def best_scan(request):
    user_uuid = request.GET['user']
    scan_type = request.GET.get('type', ModelType.TYPE_FOOT)
    user = User.objects.get(uuid=user_uuid)

    user_best_scan, user_best_scan_dist, scans_count, metrics_count = find_best_scan[scan_type](user)

    return HttpResponse(json.dumps({'scan_id': user_best_scan,
                                    'distance': user_best_scan_dist,
                                    'scans_processed': scans_count,
                                    'metrics_count': metrics_count
                                    }))
