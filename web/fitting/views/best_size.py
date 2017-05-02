from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last
from .utils import compare_by_metrics
from django.utils.datastructures import MultiValueDictKeyError
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def best_size(request):

    best_size_result = CompareResult(compare_result=CompareResult.INF)
    
    product_uuid = request.GET['product']
    user_uuid = request.GET['user']
    user = User.objects.get(uuid=user_uuid)

    try:
        scan_type = request.GET['scan_type']
    except MultiValueDictKeyError:
        scan_type = 'foot_right'
    try:
        compare_type = request.GET['compare_type']
    except MultiValueDictKeyError:
        compare_type = CompareResult.MODE_METRICS

    lasts = Last.objects.filter(product__uuid=product_uuid)

    try:
        scan = user.default_scans.get(scan_type=scan_type)
    except Scan.DoesNotExist:
        scan = Scan.objects.filter(user__uuid=user_uuid, scan_type=scan_type).first()
        user.default_scans.add(scan)
        user.save()

    for last in lasts:
        try:
            compare_result = CompareResult.objects.get(last=last, scan_1=scan)
        except CompareResult.DoesNotExist:
            compare_result = compare_by_metrics(scan, last)
        if compare_result.compare_result > best_size_result.compare_result:
            best_size_result = compare_result

    result = {
        'best_size': {
            'score': best_size_result.compare_result,
            'output_model': best_size_result.output_model
        }
    }

    return HttpResponse(json.dumps(result))
