from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last, ModelType
from .utils import compare_by_metrics
from django.utils.datastructures import MultiValueDictKeyError
import logging

logger = logging.getLogger(__name__)

compare_methods = {
    CompareResult.MODE_METRICS: compare_by_metrics
}

def compare_result_to_json(compare_result_left, compare_rsult_right):

    return {
        'score': (compare_result_left.compare_result + compare_rsult_right.compare_result) / 2,
        'output_model': compare_result_left.output_model,
        'size': str(compare_result_left.last.size)
    }


def get_foot_best_size(product_uuid, scans, compare_type):

    best_size_result = CompareResult.MIN
    best_size = None
    lasts = zip(
        Last.objects.filter(product__uuid=product_uuid, model_type=scans[0].model_type),
        Last.objects.filter(product__uuid=product_uuid, model_type=scans[1].model_type)
    )

    for pair in lasts:
        try:
            compare_result_left = CompareResult.objects.get(last=pair[0], scan_1=scans[0])
        except CompareResult.DoesNotExist:
            compare_result_left = compare_methods[compare_type](scans[0], pair[0])
        try:
            compare_result_right = CompareResult.objects.get(last=pair[1], scan_1=scans[1])
        except CompareResult.DoesNotExist:
            compare_result_right = compare_methods[compare_type](scans[1], pair[1])

        average_result = (compare_result_right.compare_result + compare_result_left.compare_result) / 2

        if average_result > best_size_result:
            best_size_result = average_result
            best_size = pair[0].size

    prev_best_size_result_left = CompareResult.objects.filter(
        last__product__uuid=product_uuid,
        last__size__numeric_value__lt=best_size.numeric_value,
        scan_1=scans[0]
    ).order_by('last__size__numeric_value').last()
    prev_best_size_result_right = CompareResult.objects.filter(
        last__product__uuid=product_uuid,
        last__size__numeric_value__lt=best_size.numeric_value,
        scan_1=scans[1]
    ).order_by('last__size__numeric_value').last()

    next_best_size_result_left = CompareResult.objects.filter(
        last__product__uuid=product_uuid,
        last__size__numeric_value__gt=best_size.numeric_value,
        scan_1=scans[0]
    ).order_by('last__size__numeric_value').first()
    next_best_size_result_right = CompareResult.objects.filter(
        last__product__uuid=product_uuid,
        last__size__numeric_value__gt=best_size.numeric_value,
        scan_1=scans[1]
    ).order_by('last__size__numeric_value').first()
    
    result = {
        'best_size': compare_result_to_json(
            CompareResult.objects.get(last__product__uuid=product_uuid, last__size=best_size, last__model_type=scans[0].model_type),
            CompareResult.objects.get(last__product__uuid=product_uuid, last__size=best_size, last__model_type=scans[0].model_type)
        )
    }

    if prev_best_size_result_left is not None:
        result['prev_best_size'] = compare_result_to_json(prev_best_size_result_left, prev_best_size_result_right)

    if next_best_size_result_left is not None:
        result['next_best_size'] = compare_result_to_json(next_best_size_result_left, next_best_size_result_right)

    return result


def get_default_scan(user, scan_type):
    try:
        scan = user.default_scans.get(model_type=scan_type)
    except Scan.DoesNotExist:
        scan = Scan.objects.filter(user__uuid=user_uuid, scan_type=scan_type).first()
        if scan is None:
            return HttpResponseBadRequest()
        user.default_scans.add(scan)
        user.save()
    return scan


@csrf_exempt
def best_size(request):

    product_uuid = request.GET['product']
    user_uuid = request.GET['user']
    user = User.objects.get(uuid=user_uuid)

    scan_type = request.GET.get('scan_type', ModelType.TYPE_LEFT_FOOT)
    compare_type = request.GET.get('compare_type', CompareResult.MODE_METRICS)
    
    scans = (get_default_scan(user, ModelType.TYPE_LEFT_FOOT), get_default_scan(user, ModelType.TYPE_RIGHT_FOOT))

    return HttpResponse(json.dumps(get_foot_best_size(product_uuid, scans, compare_type)))
