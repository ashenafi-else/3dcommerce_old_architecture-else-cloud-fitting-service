from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last
from .utils import compare_by_metrics
from django.utils.datastructures import MultiValueDictKeyError
import logging

logger = logging.getLogger(__name__)

def compare_result_to_json(compare_result):

    return {
        'score': compare_result.compare_result,
        'output_model': compare_result.output_model,
        'size': str(compare_result.last.size)
    }


@csrf_exempt
def best_size(request):

    best_size_result = CompareResult(compare_result=CompareResult.MIN)
    product_uuid = request.GET['product']
    user_uuid = request.GET['user']
    user = User.objects.get(uuid=user_uuid)

    try:
        scan_type = request.GET['scan_type']
    except MultiValueDictKeyError:
        scan_type = 'foot_right'
    try:
        compare_type = CompareResult.MODE_3D if request.GET['compare_type'] == '3d' else CompareResult.MODE_METRICS
    except MultiValueDictKeyError:
        compare_type = CompareResult.MODE_METRICS

    lasts = Last.objects.filter(product__uuid=product_uuid)

    try:
        scan = user.default_scans.get(scan_type=scan_type)
    except Scan.DoesNotExist:
        scan = Scan.objects.filter(user__uuid=user_uuid, scan_type=scan_type).first()
        if scan is None:
            return HttpResponseBadRequest()
        user.default_scans.add(scan)
        user.save()

    for last in lasts:
        try:
            compare_result = CompareResult.objects.get(last=last, scan_1=scan)
        except CompareResult.DoesNotExist:
            compare_result = compare_by_metrics(scan, last)
        if compare_result.compare_result > best_size_result.compare_result:
            best_size_result = compare_result

    try:
        prev_best_size_result = CompareResult.objects.get(
            last__product=best_size_result.last.product,
            last__size__numeric_value=best_size_result.last.size.numeric_value - 1,
            scan_1=scan
        )
    except CompareResult.DoesNotExist:
        prev_best_size_result = None

    try:
        next_best_size_result = CompareResult.objects.get(
            last__product=best_size_result.last.product,
            last__size__numeric_value=best_size_result.last.size.numeric_value + 1,
            scan_1=scan
        )
    except CompareResult.DoesNotExist:
        next_best_size_result = None

    result = {
        'best_size': compare_result_to_json(best_size_result)
    }

    if prev_best_size_result is not None:
        result['prev_best_size'] = compare_result_to_json(prev_best_size_result)

    if next_best_size_result is not None:
        result['next_best_size'] = compare_result_to_json(next_best_size_result)

    return HttpResponse(json.dumps(result))
