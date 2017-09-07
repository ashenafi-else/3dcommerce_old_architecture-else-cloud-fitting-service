from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last, ModelType, Product
from .utils import compare_by_metrics
from django.utils.datastructures import MultiValueDictKeyError
import logging

logger = logging.getLogger(__name__)


def compare_result_to_json(compare_result_left, compare_result_right):

    return {
        'score': int((compare_result_left.compare_result + compare_result_right.compare_result) / 2),
        'output_model': compare_result_right.output_model if compare_result_right.output_model else compare_result_left.output_model,
        'output_model_3d': compare_result_right.output_model_3d if compare_result_right.output_model_3d else compare_result_left.output_model_3d,
        'size': compare_result_right.last.size.value,
        'size_type': compare_result_right.last.size.model_type
    }


def get_foot_best_size(product, scans):

    best_size_result = CompareResult.MIN
    best_size = None
    lasts = zip(
        Last.objects.filter(product=product, model_type=scans[0].model_type),
        Last.objects.filter(product=product, model_type=scans[1].model_type)
    )
    for pair in lasts:
        compare_result_left = CompareResult.objects.filter(last=pair[0], scan_1=scans[0]).first()
        if compare_result_left is None:
            compare_by_metrics(scans[0], product)
            compare_result_left = CompareResult.objects.filter(last=pair[0], scan_1=scans[0]).first()
        compare_result_right = CompareResult.objects.filter(last=pair[1], scan_1=scans[1]).first()
        if compare_result_right is None:
            compare_by_metrics(scans[1], product)
            compare_result_right = CompareResult.objects.filter(last=pair[1], scan_1=scans[1]).first()

        average_result = (compare_result_right.compare_result + compare_result_left.compare_result) / 2

        if average_result > best_size_result:
            best_size_result = average_result
            best_size = pair[0].size

    prev_best_size_result_left = CompareResult.objects.filter(
        last__product=product,
        last__size__numeric_value__lt=best_size.numeric_value,
        scan_1=scans[0]
    ).order_by('last__size__numeric_value').last()
    prev_best_size_result_right = CompareResult.objects.filter(
        last__product=product,
        last__size__numeric_value__lt=best_size.numeric_value,
        scan_1=scans[1]
    ).order_by('last__size__numeric_value').last()

    next_best_size_result_left = CompareResult.objects.filter(
        last__product=product,
        last__size__numeric_value__gt=best_size.numeric_value,
        scan_1=scans[0]
    ).order_by('last__size__numeric_value').first()
    next_best_size_result_right = CompareResult.objects.filter(
        last__product=product,
        last__size__numeric_value__gt=best_size.numeric_value,
        scan_1=scans[1]
    ).order_by('last__size__numeric_value').first()

    result = {
        'best_size': compare_result_to_json(
            CompareResult.objects.filter(last__product=product, last__size=best_size, scan_1=scans[0]).first(),
            CompareResult.objects.filter(last__product=product, last__size=best_size, scan_1=scans[1]).first()
        )
    }

    if prev_best_size_result_left is not None:
        result['prev_best_size'] = compare_result_to_json(prev_best_size_result_left, prev_best_size_result_right)

    if next_best_size_result_left is not None:
        result['next_best_size'] = compare_result_to_json(next_best_size_result_left, next_best_size_result_right)

    return result


def get_default_scan(user, scan_type):
    scan = user.default_scans.filter(model_type=scan_type).first()
    if scan is None:
        scan = Scan.objects.filter(user=user, model_type=scan_type).first()
        if scan is not None:
            user.default_scans.add(scan)
            user.save()
    return scan


scan_types_functions = {
    ModelType.TYPE_FOOT: get_foot_best_size
}


@csrf_exempt
def best_size(request):

    product_uuid = request.GET['product']
    user_uuid = request.GET['user']
    scan_id = request.GET.get('scan', None)
    scan_type = request.GET.get('scan_type', ModelType.TYPE_FOOT)
    
    user = User.objects.get(uuid=user_uuid)
    
    product = Product.objects.get(uuid=product_uuid)
    if scan_id is None:
        scans = (get_default_scan(user, ModelType.TYPE_LEFT_FOOT), get_default_scan(user, ModelType.TYPE_RIGHT_FOOT))
    else:
        scans = (
            Scan.objects.filter(user=user, scan_id=scan_id, model_type=ModelType.TYPE_LEFT_FOOT).first(),
            Scan.objects.filter(user=user, scan_id=scan_id, model_type=ModelType.TYPE_RIGHT_FOOT).first()
        )

    return HttpResponse(json.dumps(scan_types_functions[scan_type](product, scans)))
